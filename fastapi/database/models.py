from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from database.database_client import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    google_id = Column(String(255), unique=True, nullable=True)
    avatar = Column(String(255), nullable=True)
    email_verified_at = Column(DateTime, nullable=True)
    password = Column(String(255), nullable=True)
    remember_token = Column(String(100), nullable=True)

    user_sessions = relationship("UserSession", back_populates="user")


class UserSession(Base):
    __tablename__ = 'user_sessions'

    id = Column(BIGINT, primary_key=True, index=True)
    session_uuid = Column(String(36), nullable=True)  # UUID format
    user_id = Column(BIGINT, ForeignKey('users.id'), nullable=True)
    last_activity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="user_sessions")
    messages = relationship("Message", back_populates="user_session")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(BIGINT, primary_key=True, index=True)
    user_session_id = Column(String(36), ForeignKey('user_sessions.id'), nullable=False)
    message_history = Column(JSON, nullable=True)

    user_session = relationship("UserSession", back_populates="messages")
