from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

import logging
from pydantic import ValidationError
from llm.llm_app import LLMApp
from dotenv import load_dotenv, find_dotenv
import os
from models import RequestSchema, ResponseSchema

load_dotenv(find_dotenv())

security = HTTPBearer()
app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")

llm_app = LLMApp()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler('app.log')]
)
logger = logging.getLogger(__name__)

def verify_token(token: str) -> dict:
    """Verify jwt token

    Args:
        token (str): jwt token

    Raises:
        HTTPException: http_error_401 if token expired
        HTTPException: http_error_403 if invalid token

    Returns:
        dict: decode payload, field: ["iss", "sub", "username", "iat", "exp"]
    """
    logger.debug(f"Verifying token: {token}")
    try:
        decode_payload = jwt.decode(token, SECRET_KEY, ["HS256"])
        logger.debug(f"Token valid: {decode_payload}")
        return decode_payload
    except jwt.ExpiredSignatureError:
        logger.error("Token expired")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        logger.error("Invalid token")
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid token")


@app.post('/chat', dependencies=[Depends(verify_token)])
async def response_items(
    request: Request,
    message: RequestSchema, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> ResponseSchema:

    logger.debug("Chat route called")
    logger.debug("Received request body: %s", await request.json())
    logger.debug("Request headers: %s", request.headers)
    token = credentials.credentials
    
    decode_payload = verify_token(token)
    username = decode_payload.get("username", " ")
    chat_history = []

    try:
        result = await llm_app.ainvoke({"question": message.message, "username": username, "chat_history": chat_history})
    except ValidationError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Validation error: {e.errors}")
    
    bot_response = result['generation']
    mood = result['mood']

    return ResponseSchema(response=bot_response, mood=mood)