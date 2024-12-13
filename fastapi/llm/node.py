from llm.chain import chain
from typing import (
    Literal,
    TypedDict
)


class State(TypedDict):
    username: str
    user_input: str
    generation: str
    mood: Literal["happy", "sad", "angry", "excited"]
    chat_history: list


def generation_node(state: State):
    username = state["username"]
    user_input = state["user_input"]
    chat_history = state["chat_history"]

    if chat_history is None:
        chat_history = [
            {"role": "user", "content": "Halo"},
            {"role": "assistant", "content": "Halo juga"}
        ]

    result = chain.invoke({"user_input": user_input, "chat_history": chat_history, "username": username})
    generation = result.generation
    mood = result.mood

    return {
        "username": username,
        "user_input": user_input,
        "generation": generation,
        "mood": mood,
        "chat_history": chat_history
    }

def insert_chat_history(state: State):
    user_input = state["user_input"]
    generation = state["generation"]
    mood = state["mood"]
    chat_history = state["chat_history"]

    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": generation})

    return {
        "generation": generation,
        "mood": mood
    }