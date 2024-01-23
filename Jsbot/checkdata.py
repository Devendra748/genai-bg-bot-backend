import weaviate
import torch
from transformers import AutoTokenizer, AutoModel
import os
import json
import torch.nn.functional as F
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)

classname = "Bgbot"

all_objects = client.data_object.get(class_name=f"{classname}")
with open('/home/h/Documents/NewTestingWorkBGDemo/jayant-sinha-chatbot/Jsbot/Fetch_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_objects, json_file, ensure_ascii=False, indent=4)