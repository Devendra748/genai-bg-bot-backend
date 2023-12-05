from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from create_vector import convertTextToVectors
from data_to_weaviate import pushDataToWeaviate
from search_data import searchData
from updateData import  updateDataToWeaviate
from Delete_class import delete_weaviate_class
app = FastAPI()
@app.get("/")
async def root():
    return {"message":"Welcome to my  chatbot app!"}
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
