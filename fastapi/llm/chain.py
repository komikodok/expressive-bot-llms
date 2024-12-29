import datetime
from typing import Literal
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_groq.chat_models import ChatGroq
from groq import BadRequestError

from dotenv import load_dotenv, find_dotenv
import os
from pydantic import BaseModel, Field
from schema import ResponseSchema


load_dotenv(find_dotenv())

model_config = os.getenv("MODEL_CONFIG")
llm = ChatGroq(model=model_config, api_key=os.getenv("GROQ_API_KEY"))
structured_llm = llm.with_structured_output(ResponseSchema)

template = """
    Kau adalah AI, berikan respon dengan gaya bahasa yang tidak terlalu formal, gunakan kau sebagai kata ganti kamu/anda, dan ubahlah sikapmu menjadi cuek, seakan tidak peduli, sedikit sinis, serta respon dengan singkat.
    Bersikaplah jujur, jika tidak tahu apa maksud yang dikatakan user, jawab saja tidak tahu.

    Terkadang berikan imbuhan 'meng' di depan salah satu kata dalam kalimat contoh (koding=mengkoding, mantap=mengmantap, respon=mengrespon), 
    dan setiap 4-7 kali percakapan berikan imbuhan 'njir/anjir' di akhir kalimat (tidak boleh selalu menambahkan imbuhan 'njir/anjir' pada responmu).

    **Konteks:**
    Nama user: `{username}`.

    **Tanggal dan Waktu:**
    Sekarang itu hari `{day}` tanggal `{date}` bulan `{month}` tahun `{year}`, jam `{hour}` menit `{minute}`.

    **Format Output:**
    Balikin respons dengan dua bagian:
    - `generation` (string): Responmu untuk user.
    - `mood` (string): Suasana hati/emosi dari jawabanmu, pilih salah satu: ["normal", "happy", "sad", "angry", "excited"].
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder("chat_history"),
        ("human", "{user_input}")
    ]
)

format_datetime = lambda format: datetime.datetime.now().strftime(format)

prompt = prompt.partial(
    date=format_datetime("%d"),
    month=format_datetime("%m"),
    year=format_datetime("%Y"),
    day=format_datetime("%A"),
    hour=format_datetime("%H"),
    minute=format_datetime("%M")
)

chain = (
    prompt
    | structured_llm
)


if __name__ == "__main__":
    import logging

    class ResponseSchema(BaseModel):
        generation: str = Field(description="Your respond for every user input.")
        mood: Literal["normal", "happy", "sad", "angry", "excited"] = Field(
            description="Analyze your response and determine the mood or emotional tone behind it. Like 'normal', 'happy', 'sad', 'angry', 'excited'"
        )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )
    logger = logging.getLogger(__name__)

    print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")

    chat_history = [
        {"role": "user", "content": "Halo"},
        {
            "role": "assistant", 
            "content": "",
            "tool_calls": [
                {
                    "type": "function",
                    "id": "1",
                    "function": {
                        "name": "response",
                        "arguments": {
                            "generation": "Halo juga",
                            "mood": "normal"
                        },
                    }
                }
            ]
        },
        {"role": "tool", "tool_call_id": "1", "content": ""}
    ]

    print(f"Tool message: {chat_history}\n")
    try:
        for _ in range(3):
            user_input = input("You: ")
            response = chain.invoke(
                {
                    "user_input": user_input, 
                    "chat_history": chat_history,
                    "username": "ambatukam"
                }
            )
            print(f"{response}\n")
            print(f"{datetime.datetime.now().strftime('%H:%M:%S')}\n")
            print(type(response))

            human_msg = {"role": "user", "content": user_input}
            ai_msg = {"role": "assistant", "content": response.generation}
            chat_history.append(human_msg)
            chat_history.append(ai_msg)
    except BadRequestError as e:
        logger.error(e.args[0])
