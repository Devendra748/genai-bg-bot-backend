from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, set_global_service_context
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.storage.storage_context import StorageContext
import weaviate
import os
from pathlib import Path
from llama_index import download_loader
from llama_index.node_parser import SentenceSplitter
from llama_index.llms import AzureOpenAI
from llama_index.embeddings import AzureOpenAIEmbedding

from dotenv import load_dotenv

WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
client = weaviate.Client(url="http://ec2-3-111-45-171.ap-south-1.compute.amazonaws.com:8080")

load_dotenv()

llm = AzureOpenAI(
    engine=os.getenv("OPENAI_AZURE_GENERATION_MODEL_DEPLOYMENT_NAME"),
    model=os.getenv("OPENAI_AZURE_GENERATION_MODEL_NAME"),
    deployment_name=os.getenv("OPENAI_AZURE_GENERATION_MODEL_DEPLOYMENT_NAME"),
    temperature=0.1,
    azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
    api_key=os.getenv("OPENAI_AZURE_API_KEY"),
    api_version=os.getenv("OPENAI_AZURE_API_VERSION"),
)

embed_model = AzureOpenAIEmbedding(
    model=os.getenv("OPENAI_AZURE_EMBEDDING_MODEL_NAME"),
    deployment_name=os.getenv("OPENAI_AZURE_EMBEDDING_MODEL_DEPLOYMENT_NAME"),
    api_key=os.getenv("OPENAI_AZURE_API_KEY"),
    azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
    api_version=os.getenv("OPENAI_AZURE_API_VERSION"),
)
PagedCSVReader = download_loader("PagedCSVReader")

loader = PagedCSVReader(encoding="utf-8")
documents = loader.load_data(file=Path('/home/nafish/Desktop/test/jayant-sinha-chatbot/Jsbot/jsbotdata/Jayant Sinha Ji Work English - Sheet3.csv'))
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
set_global_service_context(service_context)
print(len(documents))
vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="LlamaIndexEnglish"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)
print("done")
