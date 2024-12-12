from pydantic import BaseModel, Field
from typing import Literal


class RequestSchema(BaseModel):
    message: str

class ResponseSchema(BaseModel):
    generation: str = Field(description="Your respond for every user input.")
    mood: Literal["happy", "sad", "angry", "excited"] = Field(
        description="Analyze your response and determine the mood or emotional tone behind it. Like 'happy', 'sad', 'angry', 'excited'"
    )