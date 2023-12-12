import os
import weaviate
from dotenv import load_dotenv
from create_vector import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
classname = "bot"


# Weaviate configuration and Initialize the Weaviate client

def delete_weaviate_class( classname):
    try:
        client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
        client.schema.delete_class(classname)
        print(f"Class '{classname}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting class '{classname}': {e}")