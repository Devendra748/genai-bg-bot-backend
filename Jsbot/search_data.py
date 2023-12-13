import os
import weaviate
from dotenv import load_dotenv
from create_vector import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)

def searchData(classname, question,cutoff):
    try:
        print(classname)
        vectors = convertTextToVectors(question)
        response = (
            client.query
            .get(classname, ["question", "answer"])
            .with_near_vector({
                "vector": vectors[0]})
            .with_limit(1)
            .with_additional(["distance"])
            .do()
        )
    

        # Extract the distance value from the response
        distance = response['data']['Get'][classname][0]['_additional']['distance']
        similarity = (1 - distance)
        print(similarity)

        if similarity >= float(cutoff):
            answer = response['data']['Get'][classname][0]['answer']
            return answer
    except:
        return None
