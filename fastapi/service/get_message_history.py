from fastapi import Depends, HTTPException

from typing import List
from database.database_client import get_db
from sqlalchemy.orm import Session, selectinload
from database.models import User, Session as UserSession, Message

def get_message_history(user_name: str, session_id: str, db: Session = Depends(get_db)) -> List[dict]:    
    user = (
        db.query(User)
        .options(
            selectinload(User.sessions).selectinload(UserSession.messages)
        )
        .filter(User.name == user_name)
        .join(User.sessions)
        .filter(UserSession.id == session_id)
        .first()
    )
    
    if not user:
        raise HTTPException(status_code=404, detail="User or Session not found")
    
    session = next((s for s in user.sessions if s.id == session_id), None)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found for this user")

    messages = session.messages
    message_history = [message.get('message_history') for message in messages]

    return message_history