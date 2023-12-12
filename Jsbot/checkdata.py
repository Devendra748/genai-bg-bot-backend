import weaviate
import torch
from transformers import AutoTokenizer, AutoModel
import os
import json
import torch.nn.functional as F
client = weaviate.Client(url="http://ec2-15-207-103-80.ap-south-1.compute.amazonaws.com:8080")

classname = "Jsbot_cache_hindi"

all_objects = client.data_object.get(class_name=f"{classname}")
with open('/home/nafish/jayant-sinha-chatbot/Jsbot/Fetch_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_objects, json_file, ensure_ascii=False, indent=4)