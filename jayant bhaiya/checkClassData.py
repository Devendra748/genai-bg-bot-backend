import weaviate
import torch
from transformers import AutoTokenizer, AutoModel
import json
import torch.nn.functional as F
client = weaviate.Client(url="http://afcc935cf00034eedb45a56f7cccc309-430761413.ap-south-1.elb.amazonaws.com")

WEAVIATE_CLASS_NAME = "bot"

all_objects = client.data_object.get(class_name=f"{WEAVIATE_CLASS_NAME}")
with open('/home/nafish/bishan/data.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_objects, json_file, ensure_ascii=False, indent=4)
