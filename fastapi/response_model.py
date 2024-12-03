from pydantic import BaseModel, Field
from typing import (
    Literal,
    AnyStr
)

class ResponseItems(BaseModel):

    response: AnyStr = Field(description="Response dari bot dengan gaya bahasa kasual")
    mood: Literal["bahagia", "sedih", None] = Field(
        description="Mood dari bot berdasarkan response yang dihasilkan, misalnya 'bahagia', 'sedih', 'marah'",
        default=None
    )