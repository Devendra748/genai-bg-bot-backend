from create_vector import convertTextToVectors
from data_to_weaviate import pushDataToWeaviate

json_sets = []

from fastapi import FastAPI
from search_data import searchData
app = FastAPI()
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
@app.post("/push_data_to_weaviate")
def push_data_to_weaviate():
    # Call your pushDataToWeaviate function with the JSON data
    data_json = pushDataToWeaviate(json_sets)

    return {"message": data_json}
@app.post("/search_data")

def search_data(question: str, number: int):
    print(question)
    # Call your searchData function with the provided question and number
    search_result = searchData(question, number)

    return search_result
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)