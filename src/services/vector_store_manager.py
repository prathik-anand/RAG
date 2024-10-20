from src.repositories.vector_store_repository import VectorStoreRepository
from src.utils.document_processor import read_text_documents
from src.config import Config

class VectorStoreManager:
    _vector_store = None

    @classmethod
    def get_vector_store(cls):
        if cls._vector_store is None:
            vector_store_repo = VectorStoreRepository()
            try:
                cls._vector_store = vector_store_repo.get_or_create_vector_store()
            except ValueError:
                print("Vector store doesn't exist. Creating a new one...")
                texts = read_text_documents(Config.DOCUMENTS_DIRECTORY)
                cls._vector_store = vector_store_repo.get_or_create_vector_store(texts)
        return cls._vector_store
