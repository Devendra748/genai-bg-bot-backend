# import logging
# import sys
# import os.path
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# from llama_index import (
#     VectorStoreIndex,
#     SimpleDirectoryReader,
#     StorageContext,
#     load_index_from_storage,
# )
# import time

# start_time = time.time()

# # check if storage already exists
# if not os.path.exists("./storage"):
#     # load the documents and create the index
#     documents = SimpleDirectoryReader("jsbotdata").load_data()
#     index = VectorStoreIndex.from_documents(documents)
#     # store it for later
#     index.storage_context.persist()
# else:
#     # load the existing index
#     print("Loading indexes from storage")
#     storage_context = StorageContext.from_defaults(persist_dir="./storage")
#     index = load_index_from_storage(storage_context)



# # either way we can now query the index
# query_engine = index.as_query_engine()

# # Use the query from your original code
# language = "hindi"  # Change this to your desired language
# question = "tell me about hazaribagh?"
# query = f'''If the answer is not in the current context then only provide 'undefined' in response: generate the response in this format {{"question_English": "", "answer_English": "", "question_Hindi": "", "answer_Hindi": ""}}  {question}'''
# print('query = ', query)

# response = query_engine.query(query)
# print('response = ', response)

# # Store the response in store.txt
# with open("store.txt", "w") as file:
#     file.write(str(response))

import logging
import sys
import os.path
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
import time

app = FastAPI()

# check if storage already exists
if not os.path.exists("./storage"):
    # load the documents and create the index
    documents = SimpleDirectoryReader("jsbotdata").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist()
else:
    # load the existing index
    print("Loading indexes from storage")
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context)

# either way we can now query the index
query_engine = index.as_query_engine()


@app.post("/query_llama_index")
async def query_llama_index_endpoint(question: str):

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

        
