from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

class ChatMetadata(Base):
    __tablename__ = 'chat_metadata'

    chat_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Enum('active', 'inactive', name='chat_status'), default='active')
    responses = relationship("ChatHistory", back_populates="chat_metadata")

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    chat_id = Column(Integer, ForeignKey('chat_metadata.chat_id'), primary_key=True)
    user_id = Column(Integer, nullable=False) 
    request = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    sort_order = Column(Integer, nullable=False, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45))
    location = Column(String(255))
    chat_metadata = relationship("ChatMetadata", back_populates="responses")
