from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from dotenv import load_dotenv, find_dotenv
import os
from models import ResponseItems

load_dotenv(find_dotenv())

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")

@app.get('/chat')
async def response_items(
    # message:str, 
    # credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> ResponseItems:

    return ResponseItems(response="Response", mood="Mood")