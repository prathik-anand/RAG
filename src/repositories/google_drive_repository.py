from src.utils.google_drive_reader import GoogleDriveReader
from src.repositories.document_repository import DocumentRepository
from src.config import Config

class GoogleDriveRepository(DocumentRepository):
    def __init__(self):
        self.google_drive_reader = GoogleDriveReader(Config.GOOGLE_DRIVE_CREDENTIALS_FILE) 

    def create_embeddings(self, documents):
        pass 

    def read_documents(self):
        """Read all documents from Google Drive, including all folders and subfolders."""
        return self.google_drive_reader.read_documents()  # Delegate to GoogleDriveReader

    def list_files(self, folder_id=None):
        """List all files in the specified Google Drive folder or root if no ID is provided."""
        return self.google_drive_reader.list_files(folder_id)

    def list_folders(self, folder_id=None):
        """List all folders in the specified Google Drive folder or root if no ID is provided."""
        return self.google_drive_reader.list_folders(folder_id)

    def list_all_folders_and_files(self, folder_id=None):
        """Recursively list all folders and files in the specified Google Drive folder."""
        return self.google_drive_reader.list_all_folders_and_files(folder_id)
