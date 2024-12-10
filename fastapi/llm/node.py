from llm.chain import chain
from typing import (
    Literal,
    TypedDict
)


class State(TypedDict):
    username: str
    question: str
    generation: str
    mood: Literal["happy", "sad", "angry", "excited"]
    chat_history: list


def generation_node(state: State):
    username = state["username"]
    question = state["question"]
    chat_history = state["chat_history"]

    if chat_history is None:
        chat_history = [
            {"role": "user", "content": "Halo"},
            {"role": "assistant", "content": "Halo juga"}
        ]

    result = chain.invoke({"user_input": question, "chat_history": chat_history, "username": username})
    generation = result.response
    mood = result.mood

    return {
        "username": username,
        "question": question,
        "generation": generation,
        "mood": mood,
        "chat_history": chat_history
    }

def insert_chat_history(state: State):
    question = state["question"]
    generation = state["generation"]
    mood = state["mood"]
    chat_history = state["chat_history"]

    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": generation})

    return {
        "generation": generation,
        "mood": mood
    }