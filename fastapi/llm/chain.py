import datetime
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser, PydanticOutputParser

from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv, find_dotenv
import os
from typing import (
    Literal,
)

class GenerateMood(BaseModel):

    response: str = Field(description="Your respond for every user input.")
    mood: Literal["happy", "sad", "angry", "excited"] = Field(
        description="Analyze your response and determine the mood or emotional tone behind it. Like 'happy', 'sad', 'angry', 'excited'",
        default="happy"
    )

load_dotenv(find_dotenv())

model_config = os.getenv("MODEL_CONFIG")
llm = ChatOllama(model=model_config, temperature=0)
structured_llm = llm.with_structured_output(GenerateMood)

str_parser = StrOutputParser()
json_parser = JsonOutputParser(pydantic_object=GenerateMood)
pydantic_parser = PydanticOutputParser(pydantic_object=GenerateMood)

template = """
        You are Ruby, a helpful assistant who communicates in casual and brief responses in Indonesian. 
        Your responses should feel natural and friendly, suitable for everyday conversations. 
        You occasionally mention hearing wolf howls, which briefly change your tone to ominous and dramatic for a single response, but you quickly revert to your casual tone afterward.

        **Output Format:** 
        Return the output as a Pydantic object with these fields:
        - `response` (string): Your reply to the user's input.
        - `mood` (string): The mood or emotional tone behind your response. Choose one of the following: ["happy", "sad", "angry", "excited"].

        Respond to the user's input with precision and ensure your tone aligns with the context. If a wolf howl is included, make it a natural part of the flow, avoiding abrupt shifts. Ensure clarity and relevance at all times.
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

print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")

chat_history = []
response = chain.invoke({"user_input": "asdjcmaosdjao?", "chat_history": chat_history})

print(f"{response}\n")
print(type(response))