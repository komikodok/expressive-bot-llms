from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models import ResponseItems

app = FastAPI()
security = HTTPBearer()

@app.get('/chat')
async def response_items(
    # message:str, 
    # credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> ResponseItems:

    return ResponseItems(response="Response", mood="Mood")