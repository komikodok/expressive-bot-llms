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
    message_history: list


def generation_node(state: State):
    username = state.get("username")
    user_input = state.get("user_input")

    start_conversation = [
        {"role": "user", "content": "Halo"},
        {
            "role": "assistant", 
            "content": "",
            "tool_calls": [
                {
                    "type": "function",
                    "id": "first-conversation",
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
        {"role": "tool", "tool_call_id": "first-conversation", "content": ""}
    ]
    message_history = state.get("message_history", start_conversation)

    result = chain.invoke({"user_input": user_input, "chat_history": message_history, "username": username})
    generation = result.generation
    mood = result.mood

    return {
        "username": username,
        "user_input": user_input,
        "generation": generation,
        "mood": mood,
        "message_history": message_history
    }

def insert_message_history(state: State):
    user_input = state.get("user_input")
    generation = state.get("generation")
    mood = state.get("mood")
    message_history = state.get("message_history")

    message_history.append({"role": "user", "content": user_input})
    message_history.append({"role": "assistant", "content": generation})

    return {
        "generation": generation,
        "mood": mood
    }