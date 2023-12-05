import weaviate
import torch
from transformers import AutoTokenizer, AutoModel
import os
import json
import torch.nn.functional as F
client = weaviate.Client(url=os.getenv("WEAVIATE_URL"))

classname = "bot"

all_objects = client.data_object.get(class_name=f"{classname}")
with open('/home/nafish/js bo/jayant-sinha-chatbot/js bot/Fetch_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_objects, json_file, ensure_ascii=False, indent=4)
