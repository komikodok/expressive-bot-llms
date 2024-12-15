import datetime
from typing import Literal
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_groq.chat_models import ChatGroq
from groq import BadRequestError

from dotenv import load_dotenv, find_dotenv
import os
from pydantic import BaseModel, Field

class ResponseSchema(BaseModel):
    generation: str = Field(description="Your respond for every user input.")
    mood: Literal["normal", "happy", "sad", "angry", "excited"] = Field(
        description="Analyze your response and determine the mood or emotional tone behind it. Like 'normal', 'happy', 'sad', 'angry', 'excited'"
    )

load_dotenv(find_dotenv())

model_config = os.getenv("MODEL_CONFIG")
llm = ChatGroq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))
structured_llm = llm.with_structured_output(ResponseSchema)

template = """
    Namamu Ruby, asisten yang selalu merespon dengan gaya bahasa yang asik dan tidak terlalu kaku.
    Kadang-kadang, Ruby denger suara serigala. Nah, kepribadian Ruby jadi serem dan agak psikopat seakan pengen berburu serigala. 

    **Konteks:**
    Nama user itu `{username}`. Panggil nama dia jika diperlukan biar obrolannya makin asik.

    **Tanggal dan Waktu:**
    Sekarang itu day `{day}` tanggal `{date}` bulan `{month}` tahun `{year}`, jam `{hour}` menit `{minute}`.

    **Format Output:**
    Balikin respons dengan dua bagian:
    - `generation` (string): Jawaban lo buat user.
    - `mood` (string): Suasana hati/emosi dari jawaban lo, pilih dari ["normal", "happy", "sad", "angry", "excited"].

    Selalu pastiin emosi lo cocok sama konteks obrolan. Kalau ada suara serigala, masukin gaya psikopat lo itu dengan natural biar tambah unik obrolannya.
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder("chat_history"),
        ("human", "{user_input}")
    ]
)

format_datetime = datetime.datetime.now()

date, month, year = format_datetime.strftime("%d"), format_datetime.strftime("%m"), format_datetime.strftime("%Y")
day, hour, minute = format_datetime.strftime("%A"), format_datetime.strftime("%H"), format_datetime.strftime("%M")
prompt = prompt.partial(
    date=date,
    month=month,
    year=year,
    day=day,
    hour=hour,
    minute=minute
)

chain = (
    prompt
    | structured_llm
)


if __name__ == "__main__":
    import logging

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
