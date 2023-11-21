import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve API keys from environment variables
textcortex_api_key = "gAAAAABlVMzrdNpSLqEA2XAaJqE66aRxU9aBEU1TPGgQ9Wa4jXFkYb07Yy04Sz0z-gW6xp1yFZMtVIKyj7mvtwUwt1sSUY3lmuq8CYAkRuGy4EkDOuare70FnPtEdqPvELi0z4JL67-Z"

# Set your TextCortex API key
headers = {
    "Authorization": f"Bearer {textcortex_api_key}",
    "Content-Type": "application/json"
}

# Streamlit app
def main():
    st.title(" Bhagwat-geeta Chatbot")

    # Conversation history
    conversation = []

    # User input
    user_input = st.text_input("You:", key="user_input")

    # Append user input to conversation
    if st.button("Send"):
        if user_input:
            conversation.append({"role": "user", "content": user_input})

            # Call TextCortex API
            url = "https://api.textcortex.com/v1/texts/blogs"
            data = {
                "augment": None,
                "context": user_input,
                "keywords": [],
                "max_tokens": 150,
                "model": "chat-sophos-1",
                "n": 1,
                "source_lang": "en",
                "target_lang": "en",
                "temperature": 0.65,
                "title": 'Act as a bhagwat geeta expert only provide response from bhagwat geeta context if it is not from bhagwat geeta context then send response only "This is not Related to  bhagwat geeta"'
            }

            response = requests.post(url, headers=headers, json=data).json()

            # Check if the response is successful
            if 'status' in response and response['status'] == 'success':
                # Extract and append model response to conversation
                outputs = response['data']['outputs']
                if outputs:
                    model_response = outputs[0]['text']
                    conversation.append({"role": "chatbot", "content": model_response})
            else:
                st.error("Failed to get a response from TextCortex API.")

    # Display conversation
    st.text_area("Conversation:", value="\n".join([f"{msg['content']}" for msg in conversation]), height=200)

if __name__ == "__main__":
    main()
