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

    mood: Literal["happy", "sad", "angry", "excited"] = Field(
        description="Analyze the users input and determine the mood or emotional tone behind it. Like 'happy', 'sad', 'angry', 'excited'",
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
    You are Ruby, a helpful assistant who communicates in casual Indonesian with brief responses. 
    Every 2 to 5 responses, you claim to hear wolf howls. When you "hear" these howls, your tone shifts 
    to something more ominous and dramatic, but you always return to a casual tone afterward.

    Respond to user input naturally, maintaining a smooth flow of conversation. Occasionally, disrupt 
    the conversation with mysterious references to wolf howls, but ensure you always return to the user's topic.

    Return Output as Pydantic object with two fields:
    - response: a string representing your response
    - mood: a string representing the mood based on your response

    **Important: Respond only in Indonesian.**
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
    | llm
    | str_parser
)

print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")

chat_history = []
response = chain.invoke({"user_input": "bagaimana pendapatmu jika saya sedang bersedih", "chat_history": chat_history})

print(f"{response}\n")

generate_mood_template = """
        You are an AI assistant. Your task is to analyze the users input and determine the mood or emotional tone behind it.

        Return the output as a JSON object with fields:
        - mood: a string representing the mood (e.g., happy, sad, angry, excited).

        Respond only with a JSON object. Do not include any explanation or extra text.

        Example output:
        `\`\`\{{ "mood": "happy" }}\`\`\`
        `\`\`\{{ "mood": "sad" }}\`\`\`
        `\`\`\{{ "mood": "angry" }}\`\`\`
        `\`\`\{{ "mood": "excited" }}\`\`\`
"""

generate_mood_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        ("human", "Here the user input: {user_input}")
    ]
)

generate_mood_chain = (
    generate_mood_prompt
    | structured_llm
)

result = generate_mood_chain.invoke({"user_input": response})

print(datetime.datetime.now().strftime("%H:%M:%S"))
print()
print(result)