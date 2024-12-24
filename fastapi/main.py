from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

import os
import numpy as np
from pydantic import ValidationError
from llm.llm_app import LLMApp
from log.logger import logger
from service.verify_token import verify_token
from service.get_message_history import get_message_history
from database.database_client import get_db
from schema import RequestSchema, ResponseSchema

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")

llm_app = LLMApp()

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
    payload = Depends(verify_token),
    db: Session = Depends(get_db),
    ) -> ResponseSchema:

    logger.info("Chat route called")
    
    payload_dict = payload.dict()
    user_name = payload_dict.get("sub", " ")

    message_history = get_message_history(user_name=user_name, session_uuid=session_uuid, db=db)
    message_history = list(np.concatenate(message_history)) if len(message_history) > 0 else []

    try:
        result = await llm_app.ainvoke({"user_input": data.message, "username": user_name, "message_history": message_history})
        logger.info(f"Response Bot: {result}")
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Validation error: {e.errors}")
    
    generation = result.get('generation')
    mood = result.get('mood')

    return ResponseSchema(generation=generation, mood=mood)