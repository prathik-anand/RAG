from src.repositories.local_file_repository import LocalFileRepository
from src.repositories.google_drive_repository import GoogleDriveRepository

class DocumentManager:
    def __init__(self):
        self.local_repo = LocalFileRepository()
        self.google_drive_repo = GoogleDriveRepository()

    def read_local_documents(self):
        """Read all documents from the local file repository."""
        documents = self.local_repo.read_documents()
        if documents:
            print(f"Retrieved {len(documents)} documents from local files.")
        else:
            print("No documents found in local files.")
        return documents

    def read_google_drive_documents(self):
        """Read all documents from Google Drive."""
        documents = self.google_drive_repo.read_documents()
        if documents:
            print(f"Retrieved {len(documents)} documents from Google Drive.")
        else:
            print("No documents found in Google Drive.")
        return documents

    def list_all_documents(self):
        """List all documents from both repositories."""
        local_documents = self.read_local_documents()
        google_drive_documents = self.read_google_drive_documents()
        return local_documents + google_drive_documents
