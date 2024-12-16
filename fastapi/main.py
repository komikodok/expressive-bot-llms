from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import jwt

import logging
from pydantic import ValidationError
from llm.llm_app import LLMApp
from dotenv import load_dotenv, find_dotenv
import os
from models import RequestSchema, ResponseSchema, Payload

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

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Payload:
    """Verify jwt token

    Args:
        credentials: JWT token based on Authorization Bearer

    Exception:
        HTTPException: http_error_401 if token expired
        HTTPException: http_error_403 if invalid token

    Returns:
        dict: decode payload, field: ["iss", "sub", "iat", "exp"]
    """
    try:
        token = credentials.credentials
        decode_payload = jwt.decode(token, SECRET_KEY, ["HS256"])
        logger.info(f"Token valid: {decode_payload}")
        return Payload(**decode_payload)
    except jwt.ExpiredSignatureError as e:
        logger.error(f"Token expired {e}")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token {e}")
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type", "Authorization"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY
)

@app.post('/chat', dependencies=[Depends(verify_token)])
async def response_items(
    request: Request,
    data: RequestSchema,
    payload = Depends(verify_token)
    ) -> ResponseSchema:

    logger.info("Chat route called")
    logger.info("Received request body: %s", await request.json())
    
    payload_dict = payload.dict()
    username = payload_dict.get("sub", " ")

    chat_history = request.session.get("chat_history", [])

    try:
        result = await llm_app.ainvoke({"user_input": data.message, "username": username})
        request.session["chat_history"] = chat_history
        logger.info(f"Response Bot: {result}")
        logger.info(f"Chat history: {chat_history}")
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Validation error: {e.errors}")
    
    generation = result.get('generation')
    mood = result.get('mood')
    chat_history = result.get("chat_history")

    return ResponseSchema(generation=generation, mood=mood, chat_history=chat_history)