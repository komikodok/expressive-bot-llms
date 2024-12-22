from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import logging
from pydantic import ValidationError
from llm.llm_app import LLMApp
from service.verify_token import verify_token
from service.get_message_history import get_message_history
import os
from schema import RequestSchema, ResponseSchema

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")

llm_app = LLMApp()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler('app.log')]
)
logger = logging.getLogger(__name__)

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

@app.post('/chat/{session_uuid}', dependencies=[Depends(verify_token)])
async def response_items(
    data: RequestSchema,
    session_uuid: str = Path(),
    payload = Depends(verify_token)
    ) -> ResponseSchema:

    logger.info("Chat route called")
    
    payload_dict = payload.dict()
    user_name = payload_dict.get("sub", " ")
    message_history = get_message_history(user_name=user_name, session_uuid=session_uuid)
    message_history = message_history if len(message_history) > 0 else None

    try:
        result = await llm_app.ainvoke({"user_input": data.message, "username": user_name, "message_history": message_history})
        logger.info(f"Response Bot: {result}")
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Validation error: {e.errors}")
    
    generation = result.get('generation')
    mood = result.get('mood')

    return ResponseSchema(generation=generation, mood=mood)