import requests
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
OPENAI_API_KEY = "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"

def search_data(classname, number, question):
    # Replace the URL with the actual URL of your Weaviate server
    weaviate_url = "https://562d-103-199-191-126.ngrok-free.app/search_data"

    # Parameters for the request
    params = {
        "classname": classname,
        "number": number,
        "question": question
    }

    # Make a POST request to the Weaviate server
    response = requests.post(weaviate_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    # Example usage
    classname = "bot"
    number = 1
    question = "how many projects have been completed in Barhi in the year 2023"

    # Step 1: Search Data
    search_result = search_data(classname, number, question)
    print(search_result)
    print(search_result.data.data.Get.Bot[0].answer_English)

    # Check if there is a search result
    if search_result:
        # Extract relevant context from the search result
        context = search_result.get("context", "")

        # Step 2: Prompt Template
        template = f"""You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise.
        Question: {question} 
        Context: {context} 
        Answer:
        """

        prompt = ChatPromptTemplate.from_template(template)
        print(prompt)

        # Step 3: Call OpenAI Directly
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=OPENAI_API_KEY)

        # Generate the response directly from OpenAI
        response = llm.invoke(prompt.get_template_data())

        # Print the final response
        print(response)
    else:
        print("No search result.")

if __name__ == "__main__":
    main()
