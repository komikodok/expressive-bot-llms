from llm.chain import chain
from typing import (
    Literal,
    TypedDict
)


class State(TypedDict):
    question: str
    generation: str
    chat_history: list


def node(state: State):
    question = state["question"]
    chat_history = state["chat_history"]

    if chat_history is None:
        chat_history = [
            {"role": "user", "content": "Halo"},
            {"role": "assistant", "content": "Halo juga"}
        ]

    generation = chain.invoke({"question": question, "chat_history": chat_history})

    return {
        "question": question,
        "generation": generation,
        "chat_history": chat_history
    }

def insert_chat_history(state: State):
    question = state["question"]
    generation = state["generation"]
    chat_history = state["chat_history"]

    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": generation})

    return {
        "question": question,
        "generation": generation,
        "chat_history": chat_history
    }