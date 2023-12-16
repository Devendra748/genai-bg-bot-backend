# search_data_module.py

import os
from typing import List, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from llama_index import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from pydantic import BaseModel, Field
from WeaviatePush import createWeaviate
from weaviateUpdate import updateDataToWeaviate
from search_data import searchData
from llama_index_util import setup_llama_index
from llama_index.chat_engine.condense_question import (
    CondenseQuestionChatEngine,
)
from prompts import create_custom_prompt 
from llama_index.llms import ChatMessage, MessageRole
from llama_index_util import setup_llama_index

from llama_index.vector_stores import WeaviateVectorStore
import weaviate


WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)





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
    bot_name = payload.bot_name
    language = payload.language
    question = payload.question
    chat_history = payload.chat_history
    enable_cache = payload.enable_cache
    similarity_cutoff = payload.similarity_cutoff
    
    class_name = bot_name + "_cache_" + language
    create_result = createWeaviate(class_name)
    print(create_result)
    answer = None
    to_cache_data = False
    if enable_cache and create_result != class_name:
        answer = searchData(class_name, question, similarity_cutoff)

    if not answer:
        query = f"{question} in {language}"
        print('query = ', query)
        answer = get_chat_response(question, chat_history, language,bot_name)
        to_cache_data = True
        print('result = ', answer)
    data = [
        {
            "question": question,
            "answer": str(answer)
        }
    ]
    maindata = {
        "status": {
            "code": 0,
            "message": "success"
        },
        "result": data
    }

    if enable_cache and to_cache_data:
        updateDataToWeaviate(class_name, data)
    return JSONResponse(content=maindata, status_code=200)

def get_chat_response(question, chat_history, language,bot_name):
    query_engine = setup_llama_index(bot_name)
    custom_chat_history = []
    if language=="Hindi":
        language="Devanagari"
    else:
        language=language
    
    # Assuming create_custom_prompt and CondenseQuestionChatEngine functions are defined elsewhere
    custom_prompt = create_custom_prompt(language)
    for chat in chat_history:
        custom_chat_history.append(ChatMessage(
            role=MessageRole.USER,
            content=chat.question
        ))
        custom_chat_history.append(ChatMessage(
            role=MessageRole.ASSISTANT,
            content=chat.answer
        ))
    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        condense_question_prompt=custom_prompt,
        chat_history=custom_chat_history,
        verbose=True,)
    answer = chat_engine.chat(question)
    return answer


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
        index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
         )
        return {"message": "Storage updated successfully"}
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Error updating storage"}, status_code=500)








