from fastapi import FastAPI
from fastapi.responses import JSONResponse
from search_data_module import search_data, SearchDataPayload 
from delete_data_module import delete_data

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to my chatbot app!"}

@app.post("/bot/query")
async def search_data_handler(payload: SearchDataPayload):
    return await search_data(payload)

@app.post("/delete_data")
async def delete_data_handler(classname: str):
    return await delete_data(classname)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
