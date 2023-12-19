from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from search_data_module import search_data, SearchDataPayload ,update
from delete_data_module import delete_data
from weaviateUpdate import updateDataToWeaviate
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
@app.post("/update_data_to_weaviate")
async def update_data_to_weaviate(request: Request, classname: str = Query(..., title="Classname")):
    try:
        # Parse JSON data from request body
        json_sets = await request.json()
        # Use the pushDataToWeaviate function to handle data push
        data_json = updateDataToWeaviate(classname,json_sets)
        # return JSONResponse(content={"message": data_json}, status_code=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
