from src.repositories.local_file_repository import LocalFileRepository
from src.repositories.google_drive_repository import GoogleDriveRepository
from src.repositories.vector_store_repository import VectorStoreRepository
from src.utils.vectors_utils import VectorsUtils

class DocumentManager:
    def __init__(self):
        self.local_repo = LocalFileRepository()
        self.google_drive_repo = GoogleDriveRepository()
        self.vector_store_repo = VectorStoreRepository()

    def index_local_documents(self):
        """Index all documents from the local file repository."""
        documents = self.local_repo.read_documents()
        if documents:
            self.vector_store_repo.add_to_indexes(documents)
            print(f"Indexed {len(documents)} documents from local files.")
        else:
            print("No documents found in local files.")

    def index_google_drive_documents(self):
        """Index all documents from Google Drive."""
        documents = self.google_drive_repo.read_documents()
        if documents:
            self.vector_store_repo.get_or_create_vector_store(documents)
            print(f"Indexed {len(documents)} documents from Google Drive.")
        else:
            print("No documents found in Google Drive.")

    def index_all_documents(self):
        """Index documents from both local and Google Drive repositories."""
        self.index_local_documents()
        self.index_google_drive_documents()

    def list_all_documents(self):
        """List all documents from both repositories."""
        local_documents = self.local_repo.read_documents()
        google_drive_documents = self.google_drive_repo.read_documents()
        return local_documents + google_drive_documents

    def create_embeddings(self):
        """Create embeddings for all documents from both repositories."""
        local_documents = self.local_repo.read_documents()
        google_drive_documents = self.google_drive_repo.read_documents()
        all_documents = local_documents + google_drive_documents

        if all_documents:
            vectors_utils = VectorsUtils()
            embeddings = vectors_utils.create_embeddings(all_documents)
            self.vector_store_repo.add_to_indexes(embeddings)
            print(f"Created embeddings for {len(all_documents)} documents.")
        else:
            print("No documents found to create embeddings.")
