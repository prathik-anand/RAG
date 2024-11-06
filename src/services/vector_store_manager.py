from src.repositories.vector_store_repository import VectorStoreRepository
from src.services.document_manager import DocumentManager
from src.utils.log_util import Logger
from langchain_chroma import Chroma

class VectorStoreManager:
    _vector_store = None

    @classmethod
    def get_vector_store(cls):
        if cls._vector_store is None:
            Logger.log_info("Getting vector store...")
            vector_store_repo = VectorStoreRepository()
            if vector_store_repo.vector_store is None:
                Logger.log_info("Vector store does not exist. Creating embeddings...")
                dummy_vector_store = Chroma(persist_directory=vector_store_repo.persist_directory, embedding_function=vector_store_repo.embeddings)
                cls._vector_store = dummy_vector_store
                document_manager = DocumentManager()
                document_manager.create_embeddings()
            cls._vector_store = vector_store_repo.vector_store  
        return cls._vector_store
