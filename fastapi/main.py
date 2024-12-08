from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from llm.llm_app import LLMApp
from dotenv import load_dotenv, find_dotenv
import os
from models import ResponseSchema

load_dotenv(find_dotenv())

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

llm_app = LLMApp()

def verify_token(token: str) -> dict:
    """Verify jwt token

    Args:
        token (str): jwt token

    Raises:
        HTTPException: http_error_401 if token expired
        HTTPException: http_error_403 if invalid token

    Returns:
        dict: decode payload, field: ["iss", "sub", "iat", "exp"]
    """
    try:
        decode_payload = jwt.decode(token, SECRET_KEY, "HS256")
        return decode_payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid token")


@app.post('/chat')
async def response_items(
    message:str, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> ResponseSchema:

    token = credentials.credentials
    decode_payload = verify_token(token)
    username = decode_payload['sub']

    result = await llm_app.ainvoke({"question": message, "username": username}).result
    
    bot_response = result.generation
    mood = result.mood

    return ResponseSchema(response=bot_response, mood=mood).dict()