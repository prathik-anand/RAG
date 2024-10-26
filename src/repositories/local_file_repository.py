from src.utils.document_processor import read_text_documents
from src.repositories.vector_store_repository import VectorStoreRepository
from src.repositories.document_repository import DocumentRepository
import os

class LocalFileRepository(DocumentRepository):
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.vector_store_repo = VectorStoreRepository()

    def read_documents(self):
        """Read documents from the local directory."""
        return read_text_documents(self.directory_path)

    def create_embeddings(self, documents):
        """Create embeddings for the provided documents."""
        if documents:
            self.vector_store_repo.get_or_create_vector_store(documents)

    def save_embeddings(self):
        """Save the created embeddings to the vector store."""
        # This can be implemented based on how you want to manage saving
        pass
