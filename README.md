# Project Title

## Description

This project is a FastAPI-based chatbot application that integrates with Weaviate for data storage and retrieval. It leverages the OpenAI GPT-3.5 model for natural language processing and Azure services for text embedding.

## Project Structure

- **app.py**: FastAPI application defining API endpoints for handling queries and data deletion.
- **checkdata.py**: Script to fetch data from Weaviate and save it to a JSON file.
- **create_vector.py**: Script to convert text to vectors using the OpenAI GPT-3.5 model.
- **delete_class.py**: Script to delete a class in Weaviate.
- **delete_data_module.py**: Module for handling the deletion of data in Weaviate.
- **llama_index_utils.py**: Utilities for setting up and using the Llama Index for chat responses.
- **prompts.py**: Module for creating custom prompts for chat responses.
- **search_data_module.py**: Module handling the search and retrieval of data, integrating Weaviate and the Llama Index.
- **search_data.py**: Script for searching data in Weaviate based on vectors.
- **.env**: Configuration file containing environment variables.

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Set up the Weaviate server and Azure services as per the configuration in the `.env` file.
3. Run the FastAPI application: `uvicorn app:app --reload`

## Usage

### API Endpoints

- **Root Endpoint**: `/` - Welcome message.
- **Query Endpoint**: `/bot/query` - Post a search query to retrieve chatbot responses.
- **Delete Data Endpoint**: `/delete_data` - Post a class name to delete data in Weaviate.

### Scripts

- **Fetching Data**: Run `checkdata.py` to fetch data from Weaviate and save it to `Fetch_data.json`.
- **Vector Creation**: Run `create_vector.py` to convert text to vectors using the OpenAI GPT-3.5 model.
- **Data Deletion**: Run `delete_class.py` to delete a class in Weaviate.

## Configuration

This project uses an environment configuration file (`.env`) to manage sensitive information and settings. To run the project successfully, ensure that you have a valid `.env` file with the following variables properly set:

## Weaviate Configuration

- `WEAVIATE_URL`: The URL of the Weaviate server (e.g., `http://example.com:8080`).

## OpenAI Azure Configuration

- `OPENAI_AZURE_GENERATION_MODEL_DEPLOYMENT_NAME`: Deployment name for the OpenAI Azure GPT-3.5 Turbo model.
- `OPENAI_AZURE_GENERATION_MODEL_NAME`: Name of the OpenAI Azure GPT-3.5 Turbo model.
- `OPENAI_AZURE_EMBEDDING_MODEL_NAME`: Name of the OpenAI Azure Text Embedding model.
- `OPENAI_AZURE_EMBEDDING_MODEL_DEPLOYMENT_NAME`: Deployment name for the OpenAI Azure Text Embedding model.
- `OPENAI_AZURE_ENDPOINT`: The endpoint URL for the OpenAI Azure service (e.g., `https://openai.example.com`).
- `OPENAI_AZURE_API_KEY`: API key for accessing the OpenAI Azure service.
- `OPENAI_AZURE_API_VERSION`: API version for the OpenAI Azure service (e.g., `20XX-XX-XX-preview`).


# Genai-bhagavat-gita-bot
