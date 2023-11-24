import os
import weaviate
from dotenv import load_dotenv
from textToVactor import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = "http://localhost:8080"
WEAVIATE_CLASS_NAME = "wev2"


# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
def searchData(question,number):
    vectors = convertTextToVectors(question)
    print(vectors)
    response = (
        client.query
        .get(f"{WEAVIATE_CLASS_NAME}", ["question_English","answer_English","question_Hindi","answer_Hindi"])
        .with_near_vector({
            "vector": vectors[0]})
        # .with_limit(5)
        .with_limit(number)
        .do()
        )
    return(response)