import weaviate
import torch
from transformers import AutoTokenizer, AutoModel
import os
import json
import torch.nn.functional as F
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
client = weaviate.Client(url="http://ec2-52-66-220-220.ap-south-1.compute.amazonaws.com:8080")

classname = "Jsbot_cache_Hindi"

all_objects = client.data_object.get(class_name=f"{classname}")
with open('/home/nafish/Desktop/test/jayant-sinha-chatbot/Jsbot/Fetch_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_objects, json_file, ensure_ascii=False, indent=4)