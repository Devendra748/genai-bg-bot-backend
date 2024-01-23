import os
import weaviate
from dotenv import load_dotenv
load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")

# Weaviate configuration and Initialize the Weaviate client

def delete_weaviate_class( classname):
    try:
        client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
        client.schema.delete_class(classname)
        return(f"Class '{classname}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting class '{classname}': {e}")