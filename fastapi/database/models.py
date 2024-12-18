from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
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

    sessions = relationship("Session", back_populates="user")


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(String(36), primary_key=True, index=True)  # UUID format
    user_id = Column(BIGINT, ForeignKey('users.id'), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    payload = Column(Text, nullable=False)
    last_activity = Column(Integer, nullable=False)

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(BIGINT, primary_key=True, index=True)
    session_id = Column(String(36), ForeignKey('sessions.id'), nullable=False)
    metadata = Column(JSON, nullable=True)

    session = relationship("Session", back_populates="messages")
