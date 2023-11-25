import os
import weaviate
from dotenv import load_dotenv
from textToVactor import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = "http://afcc935cf00034eedb45a56f7cccc309-430761413.ap-south-1.elb.amazonaws.com"
WEAVIATE_CLASS_NAME = "bot"


# Weaviate configuration and Initialize the Weaviate client
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
def searchData(question,number):
    vectors = convertTextToVectors(question)
   
    response = (
        client.query
        .get(f"{WEAVIATE_CLASS_NAME}", ["question_English","answer_English","question_Hindi","answer_Hindi"])
        .with_near_vector({
            "vector": vectors[0]})
        # .with_limit(5)
        .with_limit(number)
       .with_additional(["distance"])
    .do()
    
    )
  
    return(response)