from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ServiceContext,
    load_index_from_storage,
)
from llama_index.llms import AzureOpenAI
from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index import set_global_service_context
from dotenv import load_dotenv
import os
from llama_index.vector_stores import WeaviateVectorStore
import weaviate

WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_URL")
client = weaviate.Client(url=WEAVIATE_CLUSTER_URL)

def setup_llama_index():
    load_dotenv()

    llm = AzureOpenAI(
        engine=os.getenv("OPENAI_AZURE_GENERATION_MODEL_DEPLOYMENT_NAME"),
        model=os.getenv("OPENAI_AZURE_GENERATION_MODEL_NAME"),
        deployment_name=os.getenv("OPENAI_AZURE_GENERATION_MODEL_DEPLOYMENT_NAME"),
        temperature=0.2,
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

    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    set_global_service_context(service_context)

    # # Load or create the llama_index
    # if not os.path.exists("./storage"):
    #     documents = SimpleDirectoryReader("jsbotdata").load_data()
    #     index = VectorStoreIndex.from_documents(documents)
    #     index.storage_context.persist()
    # else:
    #     print("Loading indexes from storage")
    #     storage_context = StorageContext.from_defaults(persist_dir="./storage")
    #     index = load_index_from_storage(storage_context)

    # return index.as_query_engine()
    vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="Jsbot"
    )
    loaded_index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = loaded_index.as_query_engine(response_mode="tree_summarize")
    return query_engine
