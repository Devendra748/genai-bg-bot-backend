# delete_data_module.py

from Delete_class import delete_weaviate_class
from fastapi.responses import JSONResponse

async def delete_data(classname: str):
    try:
        search_result = delete_weaviate_class(classname)
        return JSONResponse(content=search_result, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
