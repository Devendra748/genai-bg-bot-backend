from fastapi import FastAPI, Query, Request, UploadFile, File, Body
from fastapi.responses import JSONResponse
from search_data_module import search_data, SearchDataPayload ,update
from delete_data_module import delete_data
from weaviateUpdate import updateDataToWeaviate, updateDataToWeaviateyoutube
from WeaviatePush import createWeaviateYoutube
from search_data import searchDataYoutube
from load_csv import update_weviate_with_csv
import os
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


@app.post("/upload_csv/")
async def create_upload_file(classname: str, file: UploadFile = File(...)):
    filename = os.path.join("Bgbotdata", file.filename)
    
    # Save the file in the 'data' folder
    with open(filename, "wb") as file_object:
        file_object.write(file.file.read())
    
    update_weviate_with_csv(filename,classname)

    return {"message": "File uploaded successfully", "filename": file.filename}

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
    
@app.post("/youtube_update")
async def add_youtube_urls(data: dict = Body(...)):
    print(data["data"]["test"])
    question = data["data"]["test"][0]["question"]
    youtube_url = data["data"]["test"][0]["urlLinks"]
 
    string_format_data = [str(item) for item in youtube_url]
    array=[]
    # Print the result
    for item in string_format_data:
        array.append(item)
        print()
        print("item:",item)
        print()
        print(type(item))
        print()
    print(array)
    test =  [{
                "question": question,
                "urlLinks": array
            }]
    createWeaviateYoutube('YoutubeChache_bgbot')
    updateDataToWeaviateyoutube("YoutubeChache_bgbot",test)
    return {"message": "YouTube URLs added successfully"}


@app.get("/youtube")
async def search_youtube(query: str = Query(..., title="Search Query"), cutoff: float = Query(0.9, title="Cutoff")):
    youtube_urls = searchDataYoutube("YoutubeChache_bgbot",query, cutoff)
    return {"youtube_urls": youtube_urls}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
