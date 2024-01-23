import weaviate
import os
from dotenv import load_dotenv
from create_vector import convertTextToVectors
import logging

load_dotenv()
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")

def updateDataToWeaviate(classname,data):
    print (classname)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize Weaviate client
    client = weaviate.Client(url=WEAVIATE_CLUSTER_URL, timeout_config=(5, 15))

    class_obj = {
        "class": classname,
        "vectorizer": "none",
        "moduleConfig": {},
        "properties": [
            {"name": "question", "dataType": "text", "vectorize": True},
            {"name": "answer", "dataType": "text", "vectorize": False},
        ]
    }

    # Create the class in Weaviate if it doesn't exist
    if not client.schema.contains(class_obj):
        client.schema.create_class(class_obj)
        logger.info(f"Class '{classname}' created successfully.")

    # Split data into batches
    batch_size = 3
    data_batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

    # Initialize a counter for imported data
    imported_count = 0

    for batch_index, batch_data in enumerate(data_batches):
        with client.batch as batch:
            for i, d in enumerate(batch_data):
                try:
                    logger.info(f"Importing segment: {i + 1} in batch {batch_index + 1}")
                    properties = {
                        "question": d["question"],
                        "answer": d["answer"],
                    }

                    # Ensure vec is not None before attempting to use it
                    vec = convertTextToVectors(d["question"])
                    if vec:
                        batch.add_data_object(
                            data_object=properties,
                            class_name=classname,
                            vector=vec[0]
                        )
                        imported_count += 1
                    else:
                        logger.warning(f"Vectorization failed for segment {i + 1} in batch {batch_index + 1}")
                except Exception as e:
                    logger.error(f"Error importing segment {i + 1} in batch {batch_index + 1}: {str(e)}")

    logger.info(f"Data import completed. Imported {imported_count} data objects.")
    return "done"

def updateDataToWeaviateyoutube(classname,data):
    print (classname)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize Weaviate client
    client = weaviate.Client(url=WEAVIATE_CLUSTER_URL, timeout_config=(5, 15))

    class_obj = {
        "class": classname,
        "vectorizer": "none",
        "moduleConfig": {},
        "properties": [
            {"name": "question", "dataType": "text", "vectorize": True},
            {"name": "urlLinks", "dataType": "text[]", "vectorize": False},
            
        ]
    }

    # Create the class in Weaviate if it doesn't exist
    if not client.schema.contains(class_obj):
        client.schema.create_class(class_obj)
        logger.info(f"Class '{classname}' created successfully.")

    # Split data into batches
    batch_size = 3
    data_batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

    # Initialize a counter for imported data
    imported_count = 0

    for batch_index, batch_data in enumerate(data_batches):
        with client.batch as batch:
            for i, d in enumerate(batch_data):
                try:
                    logger.info(f"Importing segment: {i + 1} in batch {batch_index + 1}")
                    properties = {
                        "question": d["question"],
                        "urlLinks": d["urlLinks"],
                    }

                    # Ensure vec is not None before attempting to use it
                    vec = convertTextToVectors(d["question"])
                    if vec:
                        batch.add_data_object(
                            data_object=properties,
                            class_name=classname,
                            vector=vec[0]
                        )
                        imported_count += 1
                    else:
                        logger.warning(f"Vectorization failed for segment {i + 1} in batch {batch_index + 1}")
                except Exception as e:
                    logger.error(f"Error importing segment {i + 1} in batch {batch_index + 1}: {str(e)}")

    logger.info(f"Data import completed. Imported {imported_count} data objects.")
    return "done"