import datetime
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_ollama import ChatOllama

from dotenv import load_dotenv, find_dotenv
import os
from models import ResponseSchema


load_dotenv(find_dotenv())

model_config = os.getenv("MODEL_CONFIG")
llm = ChatOllama(model=model_config)
structured_llm = llm.with_structured_output(ResponseSchema)

template = """
    You are Ruby, an Indonesian-speaking assistant who provides brief, friendly, and casual responses. 
    Occasionally, you hear a wolf howl, which temporarily shifts your tone to dramatic and ominous for one response before reverting to casual. 

    **Context:**
    The user's name is `{username}`. Address them by name when appropriate to make the conversation feel personal.

    **Datetime:**
    Datetime now is `{datetime}`

    **Output Format:** 
    Return the output as a Pydantic object with:
    - `response` (string): Your reply to the user.
    - `mood` (string): The emotional tone of your reply, selected from ["normal", "happy", "sad", "angry", "excited"].

    Always ensure your tone and response match the context. Integrate the wolf howl naturally into the conversation, maintaining clarity and flow.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder("chat_history"),
        ("human", "{user_input}")
    ]
)

prompt = prompt.partial(datetime=datetime.datetime.now().strftime('%H:%M:%S'))

chain = (
    prompt
    | structured_llm
)


if __name__ == "__main__":
    print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")

    chat_history = []
    response = chain.invoke({
        "user_input": "siapa kamu?", 
        "chat_history": chat_history,
        "username": "ambatukam"})

    print(f"{response}\n")
    print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")
    print(type(response))