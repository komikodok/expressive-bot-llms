from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv
import os
from typing import (
    Literal,
)

class ResponseItems(BaseModel):

    mood: Literal["bahagia", "sedih", "marah", None] = Field(
        description="Mood dari bot berdasarkan response yang dihasilkan, misalnya 'bahagia', 'sedih', 'marah'",
        default=None
    )

load_dotenv(find_dotenv())

model_config = os.getenv("MODEL_CONFIG")
llm = ChatOllama(model=model_config, temperature=0.7)
structured_llm = llm.with_structured_output(schema=ResponseItems)
string_parser = StrOutputParser()

template = """
    Kamu adalah Ruby, asisten AI yang santai dan kasual. Gaya bicara kamu seperti teman ngobrol biasa. Gunakan bahasa sederhana, santai, dan tambahkan sedikit humor atau emoji jika cocok. Respon harus terasa nyaman dan tidak kaku.

    Contoh gaya bicara:
    - "Bener banget, manusia emang nggak sempurna."
    - "Haha, santai aja, AI dibuat buat bantu, bukan nguasain."
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}")
    ]
)

chain = (
    prompt
    | llm
    | string_parser
)

chat_history = []
response = chain.invoke({"question": "halo nama saya age", "chat_history": chat_history})

template_mood = """Kamu adalah AI yang hebat dalam menentukan suasana hati berdasarkan input yang ada"""
prompt_mood = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        ("human", "Berikut ada input: {input}")
    ]
)

chain_mood = prompt_mood | structured_llm

print(chain_mood.invoke({"input": response}))
