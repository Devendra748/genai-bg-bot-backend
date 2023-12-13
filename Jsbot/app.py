from ast import List
from dataclasses import Field
from typing import Optional
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from WeaviatePush import createWeaviate
from search_data import searchData
from weaviateUpdate import updateDataToWeaviate
from Delete_class import delete_weaviate_class
from llama_index.prompts import PromptTemplate
from llama_index.llms import ChatMessage, MessageRole
from llama_index.chat_engine.condense_question import (
    CondenseQuestionChatEngine,
)
from pydantic import BaseModel, Field
from typing import Optional,List
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ServiceContext,
    load_index_from_storage,
)
from llama_index.llms import AzureOpenAI

from dotenv import load_dotenv
import json
import logging  # Add this import statement
import sys
import os



custom_prompt = PromptTemplate(
    """\
Given a conversation (between Human and Assistant) and a follow up message from Human, \
rewrite the message to be a standalone question that captures all relevant context \
from the conversation.

<Chat History>
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
"""
)


class ChatHistory(BaseModel):
    question: str
    answer: str

class SearchDataPayload(BaseModel):
    question:str
    bot_name: str
    language: Optional[str] = Field(default="English")
    chat_history: Optional[List[ChatHistory]] = Field(default=[])
    enable_cache: Optional[bool] = Field(default=True)
    similarity_cutoff: Optional[float] = Field(default=0.9)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Load or create the llama_index
if not os.path.exists("./storage"):
    documents = SimpleDirectoryReader("jsbotdata").load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()
else:
    print("Loading indexes from storage")
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Welcome to my  chatbot app!"}

# @app.post("/query_llama_index")
# async def query_llama_index_endpoint(question: str,language:str):
#     try:
#         query =  f"{question} in {language}"
#         print('query = ', query)
#         response = query_engine.query(query)
#         print('response = ', response)
#         return response
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)

# @app.post("/push_data_to_weaviate")
# async def push_data_to_weaviate(request: Request, classname: str = Query(..., title="Classname")):
#     try:
#         # Parse JSON data from request body
#         json_sets = await request.json()

#         # Use the pushDataToWeaviate function to handle data push
#         data_json = createWeaviate(classname)
#         return JSONResponse(content={"message": data_json}, status_code=200)
#     except Exception as e:
# #         return JSONResponse(content={"error": str(e)}, status_code=500)
# @app.post("/update_data_to_weaviate")
# async def update_data_to_weaviate(request: Request, classname: str = Query(..., title="Classname")):
#     try:
#         # Parse JSON data from request body
#         json_sets = await request.json()

#         # Use the pushDataToWeaviate function to handle data push
#         data_json = updateDataToWeaviate(json_sets,classname)
#      #   return JSONResponse(content={"message": data_json}, status_code=200)
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/search_data")
async def search_data(payload: SearchDataPayload):
    # Accessing payload data
    bot_name = payload.bot_name
    language = payload.language
    question = payload.question
    chat_history = payload.chat_history
    enable_cache = payload.enable_cache
    similarity_cutoff = payload.similarity_cutoff

    class_name = bot_name + "_cache_" + language
    create_result =  createWeaviate(class_name)  
    print(create_result)
    answer = None
    to_cache_data = False
    if enable_cache and create_result != class_name:
        answer =  searchData(class_name, question, similarity_cutoff) 
    

    if  not answer:
        query =  f"{question} in {language}"
        print('query = ', query)
        answer = get_chat_response(question, chat_history, language)
        to_cache_data = True
        print('result = ', answer)
    data = [
            {
                "question": question,
                "answer": str(answer)
            }
        ]
    maindata =  {
            "status": {
                "code": 0,
                "message": "success"
            },
            "result" :  data
        }
    
    if enable_cache and to_cache_data: 
        updateDataToWeaviate(class_name, data)
    return maindata

def get_chat_response(question, chat_history, language) : 
    custom_chat_history = []
    for chat in chat_history:
        custom_chat_history.append(ChatMessage(
            role=MessageRole.USER,
            content = chat.question
        ))
        custom_chat_history.append( ChatMessage(
            role=MessageRole.ASSISTANT,
            content = chat.answer
        ))
    chat_engine = CondenseQuestionChatEngine.from_defaults(
                query_engine=query_engine,
                condense_question_prompt=custom_prompt,
                chat_history=custom_chat_history,
                verbose=True,)
    answer = chat_engine.chat(question)
    return answer
    
    
@app.post("/delete_data")
async def delete_data(classname: str):
    try:
        # Use the searchData function to handle data search
        search_result = delete_weaviate_class(classname)
        return JSONResponse(content=search_result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
