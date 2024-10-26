from typing import List
from langchain.schema import Document
from src.utils.google_drive_reader import GoogleDriveReader
from src.repositories.vector_store_repository import VectorStoreRepository
from src.repositories.document_repository import DocumentRepository
from src.config import Config

class GoogleDriveRepository(DocumentRepository):
    def __init__(self):
        self.google_drive_reader = GoogleDriveReader(Config.GOOGLE_DRIVE_CREDENTIALS_FILE) 
        self.vector_store_repo = VectorStoreRepository()

    def read_documents(self):
        """Read documents from Google Drive."""
        return self.google_drive_reader.read_documents()

    def create_embeddings(self, documents):
        """Create embeddings for the provided documents."""
        if documents:
            self.vector_store_repo.get_or_create_vector_store(documents)

    def save_embeddings(self):
        """Save the created embeddings to the vector store."""
        # This can be implemented based on how you want to manage saving
        pass
    
    def list_files(self, folder_id=None):
        """List all files in the specified Google Drive folder or root if no ID is provided."""
        return self.google_drive_reader.list_files(folder_id)

    def list_folders(self, folder_id=None):
        """List all folders in the specified Google Drive folder or root if no ID is provided."""
        return self.google_drive_reader.list_folders(folder_id)

    def list_all_folders_and_files(self, folder_id=None):
        """Recursively list all folders and files in the specified Google Drive folder."""
        return self.google_drive_reader.list_all_folders_and_files(folder_id)
