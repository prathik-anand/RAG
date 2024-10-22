from sqlalchemy.orm import Session
from src.database import SessionLocal  # Import the session management
from src.models.chat_models import ChatMetadata, ChatHistory

class ChatRepository:
    def __init__(self):
        self.session = SessionLocal()  # Create a new session

    def create_chat_metadata(self, user_id, title):
        chat_metadata = ChatMetadata(user_id=user_id, title=title)
        self.session.add(chat_metadata)
        self.session.commit()
        return chat_metadata

    def get_chat_metadata(self, chat_id):
        return self.session.query(ChatMetadata).filter(ChatMetadata.chat_id == chat_id).first()

    def get_chat_history_count(self, chat_id):
        return self.session.query(ChatHistory).filter(ChatHistory.chat_id == chat_id).count()

    def add_chat_history(self, chat_id, user_id, request, response, sort_order, ip_address, location):
        chat_history = ChatHistory(chat_id=chat_id, user_id=user_id, request=request, response=response, sort_order=sort_order, ip_address=ip_address, location=location)
        self.session.add(chat_history)
        self.session.commit()
        return chat_history

    def get_chat_history_by_chat_id_and_user_id(self, chat_id, user_id):
        return self.session.query(ChatHistory).filter(ChatHistory.chat_id == chat_id, ChatHistory.user_id == user_id).all()
