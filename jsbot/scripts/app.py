from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from create_vector import convertTextToVectors
from data_to_weaviate import pushDataToWeaviate
from search_data import searchData
from updateData import updateDataToWeaviate
from Delete_class import delete_weaviate_class
from openai_logic import call_openai
from dotenv import load_dotenv
import json
import logging  # Add this import statement
import sys
import os
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

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

@app.post("/query_llama_index")
async def query_llama_index_endpoint(question: str):
    try:
        # query = f"If the answer is not in the current context then only provide 'undefined' in response: generate the response in {language} language\n {question}"
        query = f'''If the answer is not in the current context then only provide 'undefined' in response: generate the response in JSON format {{"question_English": "", "answer_English": "", "question_Hindi": "", "answer_Hindi": ""}}  {question}'''
        print('query = ', query)

        response = query_engine.query(query)

        print('response = ', response)
        print(type(response))

        json_string = json.dumps(response, default=lambda o: o.__dict__, indent=2)
        print(type(json_string))

        json_data = json.loads(json_string)
        print('json_data =',json_data)

        json_dataresp = json.loads(json_data['response'])

        print(json_dataresp)
        return json_dataresp

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



# @app.post("/call_openai")
# async def call_openai_endpoint(question: str, number: int, classname: str, language: str):
#     try:
#         search_result = searchData(question, number, classname)
#         print(search_result)

#         bot_data = search_result['data'].get('Get', {}).get('Testing', [])
#         if bot_data:
#             context = bot_data[0].get('question_English', '')
#             print(context)

#             template = f"""You are an assistant for question-answering tasks. 
#             Use the following pieces of retrieved context to answer the question. 
#             If you don't know the answer, just say that you don't know. 
#             Use three sentences maximum and keep the answer concise.
#             Generate the answer in {language}.
#             Question: {question} 
#             Context: {context}  
#             Answer:
#             """

#             resp_data = call_openai(template)
#             return JSONResponse(content={"message": f"Generated Response : {resp_data}"}, status_code=200)
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)



@app.post("/push_data_to_weaviate")
async def push_data_to_weaviate(request: Request, classname: str = Query(..., title="Classname")):
    try:
        # Parse JSON data from request body
        json_sets = await request.json()

        # Use the pushDataToWeaviate function to handle data push
        data_json = pushDataToWeaviate(json_sets, classname)
        return JSONResponse(content={"message": data_json}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
@app.post("/update_data_to_weaviate")
async def update_data_to_weaviate(request: Request, classname: str = Query(..., title="Classname")):
    try:
        # Parse JSON data from request body
        json_sets = await request.json()

        # Use the pushDataToWeaviate function to handle data push
        data_json = updateDataToWeaviate(json_sets,classname)
     #   return JSONResponse(content={"message": data_json}, status_code=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/search_data")
async def Search_data(question: str, number: int, classname: str):
  
        # Use the searchData function to handle data search
        search_result = searchData(question, number, classname)
        print(classname)
        return JSONResponse(content=search_result, status_code=200)

@app.post("/delete_data")
async def delete_data( classname: str):
    try:
        # Use the searchData function to handle data search
        search_result = delete_weaviate_class(classname)
        return {JSONResponse(content=search_result, status_code=200),"Class 'bot' deleted successfully."}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
