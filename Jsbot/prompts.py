from llama_index.prompts import PromptTemplate

def create_custom_prompt(language: str) -> PromptTemplate:
    return PromptTemplate(
        f"""\
Given a conversation (between Human and Assistant) and a follow up message from Human, \
rewrite the message to be a standalone question that captures all relevant context \
from the conversation. Also, the standalone question should be prefixed with 'Answer in {language}.
Don't repeat the line or words that you already mentioned in the answer.
Use punctuation when providing the answer and separate the lines with punctuation.
use [
पूर्ण विराम (Full Stop) - । or .
कमा (Comma) - ,
विसर्ग (Colon) - :
अंतरक्षेप (Semicolon) - ;
विसर्जन (Exclamation Mark) - !
प्रश्न चिन्ह (Question Mark) - ?
अनुबन्धक (Quotation Marks) - " "
अंध विसर्जन (Ellipsis) - ...
एन डैश (En Dash) - -
एम डैश (Em Dash) - — ]
punctuations.
<Chat History>
{{chat_history}}

<Follow Up Message>
{{question}}

<Standalone question> 
"""
    )
