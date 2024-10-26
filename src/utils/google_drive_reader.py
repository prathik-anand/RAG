import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.schema import Document
from src.config import Config
from src.utils.logger import Logger


class GoogleDriveReader:
    def __init__(self):
        self.credentials_file = Config.GOOGLE_DRIVE_CREDENTIALS_FILE
        self.service = self.authenticate()

    def authenticate(self):
        """Authenticate and create the Google Drive service."""
        creds = service_account.Credentials.from_service_account_file(
            self.credentials_file,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=creds)

    def list_files(self, folder_id=None):
        """List files in the specified Google Drive folder."""
        query = f"'{folder_id}' in parents" if folder_id else "trashed = false"
        try:
            results = self.service.files().list(
                q=query,
                fields="files(id, name, mimeType)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def list_folders(self, folder_id=None):
        """List folders in the specified Google Drive folder."""
        query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'" if folder_id else "mimeType='application/vnd.google-apps.folder' and trashed = false"
        try:
            results = self.service.files().list(
                q=query,
                fields="files(id, name)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def read_documents(self):
        """Read documents from Google Drive and return as a list of Document objects."""
        documents = []
        files = self.list_files()
        
        for file in files:
            file_id = file['id']
            file_name = file['name']
            mime_type = file['mimeType']
            print(f'Reading file: {file_name} (ID: {file_id})')

            if mime_type == 'application/vnd.google-apps.document':
                # Google Docs
                content = self.service.documents().get(documentId=file_id).execute()
                text = content.get('body').get('content')
                # Process text to extract content
                documents.append(Document(page_content=text, metadata={"name": file_name}))
            elif mime_type == 'application/pdf':
                # PDF
                documents.append(PyPDFLoader(file_id).load())
            elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                # Word Document
                documents.append(Docx2txtLoader(file_id).load())
            elif mime_type == 'text/plain':
                # Text File
                documents.append(TextLoader(file_id).load())
            else:
                print(f'Skipping unsupported file type: {mime_type}')

        return documents

    def list_all_folders_and_files(self, folder_id=None):
        """Recursively list all folders and files in the specified Google Drive folder."""
        all_items = []
        folders = self.list_folders(folder_id)
        files = self.list_files(folder_id)

        all_items.extend(folders)
        all_items.extend(files)

        for folder in folders:
            # Recursively list items in each subfolder
            all_items.extend(self.list_all_folders_and_files(folder['id']))  # Assuming folder has an 'id' attribute

        return all_items
