import os
import weaviate
from dotenv import load_dotenv
from create_vector import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_CLASS_NAME = "bot"


# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
def searchData(question,number,classname):
    vectors = convertTextToVectors(question)
   
    response = (
        client.query
        .get(classname, ["question_English","answer_English","question_Hindi","answer_Hindi"])
        .with_near_vector({
            "vector": vectors[0]})
        # .with_limit(5)
        .with_limit(number)
       .with_additional(["distance"])
    .do()
    
    )
  
    return(response)