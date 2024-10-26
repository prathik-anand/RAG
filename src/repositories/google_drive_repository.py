from typing import List
from langchain.schema import Document
from src.utils.google_drive_reader import GoogleDriveReader
from src.repositories.vector_store_repository import VectorStoreRepository
from src.repositories.document_repository import DocumentRepository

class GoogleDriveRepository(DocumentRepository):
    def __init__(self, folder_id: str, credentials_file: str):
        self.folder_id = folder_id
        self.credentials_file = credentials_file
        self.google_drive_reader = GoogleDriveReader(folder_id, credentials_file)
        self.vector_store_repo = VectorStoreRepository()

    def read_documents(self) -> List[Document]:
        """Read documents from Google Drive."""
        return self.google_drive_reader.read_documents()

    def create_embeddings(self, documents: List[Document]):
        """Create embeddings for the provided documents."""
        if documents:
            self.vector_store_repo.get_or_create_vector_store(documents)

    def save_embeddings(self):
        """Save the created embeddings to the vector store."""
        # This can be implemented based on how you want to manage saving
        pass
    
    def list_files(self):
        """List all files in the Google Drive folder."""
        return self.google_drive_reader.list_files()
    
    def list_folders(self):
        """List all folders in the Google Drive folder."""
        return self.google_drive_reader.list_folders()
