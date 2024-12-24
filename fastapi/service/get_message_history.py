from fastapi import Depends, HTTPException

from typing import List
from database.database_client import get_db
from sqlalchemy.orm import Session, selectinload
from database.models import User, UserSession, Message

def get_message_history(user_name: str, session_uuid: str, db: Session = Depends(get_db)) -> List[dict]:    
    user = (
        db.query(User)
        .options(
            selectinload(User.user_sessions).selectinload(UserSession.messages)
        )
        .filter(User.name == user_name)
        .join(User.user_sessions)
        .filter(UserSession.session_uuid == session_uuid)
        .first()
    )
    
    if not user:
        raise HTTPException(status_code=404, detail="User or Session not found")
    
    user_session = next((s for s in user.user_sessions if s.session_uuid == session_uuid), None)
    
    if not user_session:
        raise HTTPException(status_code=404, detail="Session uuid not found for this user")

    messages = user_session.messages
    message_history = [message.message_history for message in messages]

    return message_history