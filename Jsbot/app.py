from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from search_data_module import search_data, SearchDataPayload ,update
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

@app.post("/update-storage")
async def update_storage_data_handler(request: Request, filename: str,folder: str,bot_name: str):
    return await update(request, filename,folder,bot_name)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
