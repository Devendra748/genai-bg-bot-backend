import weaviate
import os
import json
from dotenv import load_dotenv
from textToVactor import convertTextToVectors

load_dotenv()
WEAVIATE_CLUSTER_URL = "http://localhost:8080"
WEAVIATE_CLASS_NAME = "bafish"

def pushDataToWeaviate(data):
    print(data)
    # Your JSON data with a larger number of items
    print(len(data))

    # Initialize Weaviate client
    client = weaviate.Client(url = WEAVIATE_CLUSTER_URL,
    timeout_config = (5, 15))

    # client.schema.delete_all()

    # Define the class name and schema
    # client.schema.delete_class(WEAVIATE_CLASS_NAME)

    class_obj = {
        "class": WEAVIATE_CLASS_NAME,
        "vectorizer": "none",
        "moduleConfig": {}
    }

    # Create the class in Weaviate
    try:
        client.schema.create_class(class_obj)
        print(f"Class '{WEAVIATE_CLASS_NAME}' created successfully.")
    except weaviate.RequestError as e:
        if e.status_code == 409:
            print(f"Class '{WEAVIATE_CLASS_NAME}' already exists.")
        else:
            print(f"Error creating class: {e}")


    # Tokenize the input texts
    # embeddings, data_batches = convertTextToVectors(data)

    # Split your data into batches
    batch_size = 3
    data_batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]


    # Initialize a counter for imported data
    imported_count = 0

    for batch_index, batch_data in enumerate(data_batches):
        with client.batch as batch:
            for i, d in enumerate(batch_data):
                try:
                    print(f"Importing segment: {i + 1} in batch {batch_index + 1}")
                    properties = {
                        "question_English": d["question_English"],
                        "answer_English": d["answer_English"],
                        "question_Hindi": d["question_Hindi"],
                        "answer_Hindi": d["answer_Hindi"],
                    }
                    vec = convertTextToVectors(d["question_English"])
                    batch.add_data_object(
                        data_object=properties,
                        class_name=WEAVIATE_CLASS_NAME,
                     
                        vector=vec[0]
                    )
                    imported_count += 1
                except Exception as e:
                    print(f"Error importing segment {i + 1} in batch {batch_index + 1}: {str(e)}")

    print("Data import completed.",)

    return "done"    