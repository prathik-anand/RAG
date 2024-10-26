from src.utils.google_drive_reader import GoogleDriveReader
from src.repositories.vector_store_repository import VectorStoreRepository
from src.config import Config

class DocumentService:
    def __init__(self, folder_id: str):
        self.folder_id = folder_id
        self.google_drive_reader = GoogleDriveReader(folder_id, 'path/to/credentials.json')
        self.vector_store_repo = VectorStoreRepository()

    def process_documents(self):
        """Read documents from Google Drive, create embeddings, and store them."""
        documents = self.google_drive_reader.read_documents()
        if documents:
            # Create embeddings and store in vector store
            self.vector_store_repo.get_or_create_vector_store(documents)
        else:
            print("No documents found to process.")
