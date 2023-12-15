# search_data_module.py

from typing import List, Optional
from fastapi import HTTPException
from fastapi.responses import JSONResponse
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





class ChatHistory(BaseModel):
    question: str
    answer: str

class SearchDataPayload(BaseModel):
    question: str
    bot_name: str
    language: Optional[str] = Field(default="English")
    chat_history: Optional[List[ChatHistory]] = Field(default=[])
    enable_cache: Optional[bool] = Field(default=True)
    similarity_cutoff: Optional[float] = Field(default=0.9)

query_engine = setup_llama_index()


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
        answer = get_chat_response(question, chat_history, language)
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

def get_chat_response(question, chat_history, language):
    custom_chat_history = []
    
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
