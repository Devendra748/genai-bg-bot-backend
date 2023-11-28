import os
import weaviate
from dotenv import load_dotenv
from create_vector import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_CLASS_NAME = "bot"


# Weaviate configuration and Initialize the Weaviate client

def delete_weaviate_class():
    try:
        client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
        client.schema.delete_class(WEAVIATE_CLASS_NAME)
        print(f"Class '{WEAVIATE_CLASS_NAME}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting class '{WEAVIATE_CLASS_NAME}': {e}")