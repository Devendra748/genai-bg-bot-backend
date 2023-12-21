# search_data_module.py

import logging
import os
import sys
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from llama_index import PromptTemplate, ServiceContext, SimpleDirectoryReader, StorageContext, VectorStoreIndex, set_global_service_context

from pydantic import BaseModel, Field
from WeaviatePush import createWeaviate
from weaviateUpdate import updateDataToWeaviate
from search_data import searchData
from llama_index_util import setup_llama_index
from llama_index.chat_engine.condense_question import (
    CondenseQuestionChatEngine,
)
from prompts import create_custom_prompt 
from llama_index.llms import ChatMessage, MessageRole,AzureOpenAI
from llama_index_util import setup_llama_index
from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index.vector_stores import WeaviateVectorStore
import weaviate

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
llm = AzureOpenAI(
        engine=os.getenv("OPENAI_AZURE_GENERATION_MODEL_DEPLOYMENT_NAME"),
        model=os.getenv("OPENAI_AZURE_GENERATION_MODEL_NAME"),
        deployment_name=os.getenv("OPENAI_AZURE_GENERATION_MODEL_DEPLOYMENT_NAME"),
        temperature=0.2,
        azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
        api_key=os.getenv("OPENAI_AZURE_API_KEY"),
        api_version=os.getenv("OPENAI_AZURE_API_VERSION"),
    )

embed_model = AzureOpenAIEmbedding(
        model=os.getenv("OPENAI_AZURE_EMBEDDING_MODEL_NAME"),
        deployment_name=os.getenv("OPENAI_AZURE_EMBEDDING_MODEL_DEPLOYMENT_NAME"),
        api_key=os.getenv("OPENAI_AZURE_API_KEY"),
        azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
        api_version=os.getenv("OPENAI_AZURE_API_VERSION"),
    )


client = weaviate.Client(url=WEAVIATE_CLUSTER_URL )

custom_prompt = PromptTemplate(
    """
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question in same language as follow up message given.
​
<Chat History>
{chat_history}
​
<Follow Up Message>
{question}
​
<Standalone question>
"""
)



class ChatHistory(BaseModel):
    question: str
    answer: str

class SearchDataPayload(BaseModel):
    question: str
    bot_name: str
    language: Optional[str]
    chat_history: Optional[List[ChatHistory]] = Field(default=[])
    enable_cache: Optional[bool] = Field(default=True)
    similarity_cutoff: Optional[float] = Field(default=0.9)






async def search_data(payload: SearchDataPayload):
    # Extracting data from the payload
    bot_name = payload.bot_name
    language = payload.language
    question = payload.question
    chat_history = payload.chat_history
    enable_cache = payload.enable_cache
    similarity_cutoff = payload.similarity_cutoff
    
    # Creating a class name
    class_name = bot_name + "_cache_test_new2"
    
    # Creating Weaviate instance
    create_result = createWeaviate(class_name)
    print(create_result)
    
    answer = None
    to_cache_data = False
    custom_chat_history = ""

    # Creating a custom chat history string
    for chat in chat_history:
        custom_chat_history += f"User: {chat.question}\n"
        custom_chat_history += f"AI: {chat.answer} \n"
    
    # Generating a standalone question using llm
    standalone_question = llm.predict(custom_prompt, question=question, chat_history=custom_chat_history)
    print("standalone question:", standalone_question)
    
    # Checking if caching is enabled and create_result is not equal to class_name
    if enable_cache and create_result != class_name:
        answer = searchData(class_name, standalone_question, similarity_cutoff)

    # If no answer is found, retrieve the response using get_chat_response
    if not answer:
        query = f"{question}"
        print('query = ', query)
        answer = get_chat_response(standalone_question, chat_history, language, bot_name)
        to_cache_data = True
        print('result = ', answer)
    
    # Formatting the data for the response
    data = [{"question": standalone_question, "answer": str(answer)}]
    maindata = {"status": {"code": 0, "message": "success"}, "result": data}

    # If caching is enabled and new data needs to be cached, update Weaviate
    if enable_cache and to_cache_data:
        updateDataToWeaviate(class_name, data)
    
    # Returning the response
    return JSONResponse(content=maindata, status_code=200)

def get_chat_response(question, chat_history, language, bot_name):
    # Template for the summary
    new_summary_tmpl_str = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the information from multiple sources and not prior knowledge and do not include file path in your final answer. "
        "Try to give answer in bullet points and prioritize it based on the recommendation amount, putting the one with the highest recommendation amount first,  First translate your full answer in {lang} language and give answer only in {lang} language\n"
        "Query: {query_str}\n"
        "Answer: "
    )
    if language == "Hindi":
        language = "Hindi Devanagari"
    else:
        language = language
    new_summary_tmpl_str = new_summary_tmpl_str.replace("{lang}", language)
    new_summary_tmpl = PromptTemplate(new_summary_tmpl_str)
    print(new_summary_tmpl)

    # Setting up llama index
    query_engine = setup_llama_index("LlamaIndexEnglish")
    
    # Handling language conversion
    if language == "Hindi":
        language = "Hindi Devanagari"
    else:
        language = language
    
    # Replacing the language in the template
    new_summary_tmpl_str = new_summary_tmpl_str.replace("{lang}", language)
    
    # Creating a custom prompt
    custom_prompt = create_custom_prompt(language)
    
    # Updating llama index prompts
    query_engine.update_prompts({"response_synthesizer:summary_template": new_summary_tmpl})
    
    # Querying the engine for the answer
    answer = query_engine.query(question)
    print("=========================================================")
    print(answer)
    print("=========================================================")
    
    # Returning the response
    return answer.response
async def update(request: Request, filename: str,folder: str,bot_name: str):
    try:
        # Get the text data from the request body
        data = await request.body()
        text_data = data.decode('utf-8')
        # Specify the folder to store the file
        folder_name = folder  # Replace with your desired folder name
        folder_path = os.path.join(os.getcwd(), folder_name)
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # Create a new file or open an existing file in append mode and write the text data to it
        file_path = os.path.join(folder_path, filename)
        if os.path.exists(file_path):
            with open(file_path, 'a') as file:
                # Append the new text_data to the existing file content
                file.write("\n" + text_data)
        else:
            with open(file_path, 'w') as file:
                # Create a new file and write the text data to it
                file.write(text_data)
        client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
        documents = SimpleDirectoryReader(folder).load_data()
        vector_store = WeaviateVectorStore(
        weaviate_client=client, index_name=bot_name
         )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
        set_global_service_context(service_context)
        index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context,
         )
        return {"message": "Storage updated successfully"}
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Error updating storage"}, status_code=500)








