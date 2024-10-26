import os
from typing import List
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.schema import Document

class GoogleDriveReader:
    def __init__(self, folder_id: str, credentials_file: str):
        self.folder_id = folder_id
        self.credentials_file = credentials_file
        self.service = self.authenticate()

    def authenticate(self):
        """Authenticate and create the Google Drive service."""
        creds = service_account.Credentials.from_service_account_file(
            self.credentials_file,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=creds)

    def list_files(self) -> List[dict]:
        """List files in the specified Google Drive folder."""
        try:
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents",
                fields="files(id, name, mimeType)"
            ).execute()
            return results.get('files', [])
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def read_documents(self) -> List[Document]:
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
                # (You may need to implement a function to convert Google Docs content to plain text)
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
