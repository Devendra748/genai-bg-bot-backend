import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set your OpenAI API key
openai.api_key = "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"

# Streamlit app
def main():
    st.title("Bhagavad Gita Chatbot")

    # Conversation history
    conversation = []

    # User input
    user_input = st.text_input("You:", key="user_input")

    # Append user input to conversation
    if st.button("Send"):
        if user_input:
            conversation.append({"role": "user", "content": user_input})

            # Call OpenAI GPT-3.5-turbo
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                messages=conversation,
                max_tokens=150
            )

            # Append model response to conversation
            conversation.append({"role": "chatbot", "content": response['choices'][0]['message']['content']})

    # Display conversation
    st.text_area("Conversation:", value="\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation]), height=200)

if __name__ == "__main__":
    main()
