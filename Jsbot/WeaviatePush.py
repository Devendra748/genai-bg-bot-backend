import weaviate
import os
from dotenv import load_dotenv

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")

def createWeaviate(class_name):
    client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)
    properties = [
        {"dataType": ["text"], "name": "question"},
        {"dataType": ["text"], "name": "answer"},
    ]
    class_obj = {
        "class": class_name,
        "vectorizer": "none",
        "properties": properties,
    }

    # Check if the class already exists
    if not client.schema.contains(class_obj):
        
            # Add the schema
            client.schema.create_class(class_obj)
            return class_name
    else:
        return f"Class '{class_name}' already exists."

