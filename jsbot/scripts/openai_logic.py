# openai_logic.py
import requests
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
from dotenv import load_dotenv

load_dotenv()

helicone_key = os.getenv("HELICONE_KEY")
helicone_username = os.getenv("Helicone_USER_NAME")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = OpenAI(
    temperature=0,
    model_name="gpt-3.5-turbo",
    headers={
        "Helicone-Auth": helicone_key,
        "Helicone-User-Id": helicone_username
    }
)

def call_openai(template):
    with get_openai_callback() as cb:
        try:
            resp_data = llm(template)
            return resp_data
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            print(cb)
            return None
