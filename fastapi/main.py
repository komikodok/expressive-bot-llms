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
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler('app.log')]
)
logger = logging.getLogger(__name__)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify jwt token

    Args:
        credentials: JWT token based on Authorization Bearer

    Raises:
        HTTPException: http_error_401 if token expired
        HTTPException: http_error_403 if invalid token

    Returns:
        dict: decode payload, field: ["iss", "sub", "iat", "exp"]
    """
    try:
        token = credentials.credentials
        decode_payload = jwt.decode(token, SECRET_KEY, ["HS256"])
        logger.info(f"Token valid: {decode_payload}")
        return decode_payload
    except jwt.ExpiredSignatureError as e:
        logger.error(f"Token expired {e}")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token {e}")
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid token")


@app.post('/chat', dependencies=[Depends(verify_token)])
async def response_items(
    request: Request,
    message: RequestSchema,
    decode_payload = Depends(verify_token)
    ) -> ResponseSchema:

    logger.info("Chat route called")
    logger.info("Received request body: %s", await request.json())
    
    username = decode_payload.get("sub", " ")
    chat_history = []

    try:
        result = await llm_app.ainvoke({"user_input": message.message, "username": username, "chat_history": chat_history})
        logger.info(f"Response Bot: {result}")
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Validation error: {e.errors}")
    
    generation = result['generation']
    mood = result['mood']

    return ResponseSchema(generation=generation, mood=mood)