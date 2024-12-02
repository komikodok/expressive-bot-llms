from pydantic import BaseModel


class ResponseItems(BaseModel):

    response: str
    mood: str