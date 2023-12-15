from llama_index.prompts import PromptTemplate

def create_custom_prompt(language: str) -> PromptTemplate:
    return PromptTemplate(
        f"""\
Given a conversation (between Human and Assistant) and a follow up message from Human, \
rewrite the message to be a standalone question that captures all relevant context \
from the conversation.Also the standalone question should be prefixed with 'Answer in {language}.

<Chat History>
{{chat_history}}

<Follow Up Message>
{{question}}

<Standalone question> 
"""
    )
