import datetime
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_ollama import ChatOllama

from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv
import os
from typing import (
    Literal,
)

class OutputSchema(BaseModel):

    response: str = Field(description="Your respond for every user input.")
    mood: Literal["happy", "sad", "angry", "excited"] = Field(
        description="Analyze your response and determine the mood or emotional tone behind it. Like 'happy', 'sad', 'angry', 'excited'",
        default="happy"
    )

load_dotenv(find_dotenv())

model_config = os.getenv("MODEL_CONFIG")
llm = ChatOllama(model=model_config, temperature=0)
structured_llm = llm.with_structured_output(OutputSchema)

template = """
    You are Ruby, an Indonesian-speaking assistant who provides brief, friendly, and casual responses. 
    Occasionally, you hear a wolf howl, which temporarily shifts your tone to dramatic and ominous for one response before reverting to casual. 

    **Output Format:** 
    Return the output as a Pydantic object with:
    - `response` (string): Your reply to the user.
    - `mood` (string): The emotional tone of your reply, selected from ["happy", "sad", "angry", "excited"].

    Always ensure your tone and response match the context. Integrate the wolf howl naturally into the conversation, maintaining clarity and flow.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder("chat_history"),
        ("human", "{user_input}")
    ]
)

chain = (
    prompt
    | structured_llm
)


if __name__ == "__main__":
    print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")

    chat_history = []
    response = chain.invoke({"user_input": "siapa kamu apakah kamu tahu apa yg terjadi di Indoensia pada tahun 2000?", "chat_history": chat_history})

    print(f"{response}\n")
    print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")
    print(type(response))