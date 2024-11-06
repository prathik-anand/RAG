from src.repositories.local_file_repository import LocalFileRepository
from src.repositories.google_drive_repository import GoogleDriveRepository
from src.repositories.confluence_repository import ConfluenceRepository
from src.repositories.vector_store_repository import VectorStoreRepository
from src.utils.log_util import Logger
from src.utils.vectors_utils import VectorsUtils

class DocumentManager:
    def __init__(self):
        self.local_repo = LocalFileRepository()
        self.google_drive_repo = GoogleDriveRepository()
        self.confluence_repo = ConfluenceRepository()
        self.vector_store_repo = VectorStoreRepository()

    def read_local_documents(self):
        """Read all documents from the local file repository."""
        try:
            documents = self.local_repo.read_documents()
            if documents:
                Logger.info(f"Retrieved {len(documents)} documents from local files.")
            else:
                Logger.info("No documents found in local files.")
            return documents
        except Exception as e:
            Logger.log_error(f"Error reading local documents: {str(e)}")
            return []

    def read_google_drive_documents(self):
        """Read all documents from Google Drive."""
        try:
            documents = self.google_drive_repo.read_documents()
            if documents:
                Logger.info(f"Retrieved {len(documents)} documents from Google Drive.")
            else:
                Logger.info("No documents found in Google Drive.")
            return documents
        except Exception as e:
            Logger.log_error(f"Error reading Google Drive documents: {str(e)}")
            return []

    def read_confluence_documents(self):
        """Read all documents from Confluence."""
        try:
            documents = self.confluence_repo.read_documents()
            if documents:
                Logger.info(f"Retrieved {len(documents)} documents from Confluence.")
            else:
                Logger.info("No documents found in Confluence.")
            return documents
        except Exception as e:
            Logger.log_error(f"Error reading Confluence documents: {str(e)}")
            return []

    def read_all_documents(self):
        """Read all documents from local files, Google Drive, and Confluence."""
        all_documents = []
        all_documents.extend(self.local_repo.read_documents())
        all_documents.extend(self.google_drive_repo.read_documents())
        all_documents.extend(self.confluence_repo.read_documents())
        Logger.info(f"Total documents retrieved: {len(all_documents)}")
        return all_documents

    def create_embeddings(self):
        """Create embeddings for all documents from all sources."""
        documents = self.read_all_documents()
        if documents:
            Logger.info("Creating embeddings for the retrieved documents...")
            self.vector_store_repo.add_to_indexes(documents)
        else:
            Logger.warning("No documents available to create embeddings.")
