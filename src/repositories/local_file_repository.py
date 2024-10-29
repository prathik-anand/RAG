import os
from src.utils.document_processor import read_text_documents
from src.repositories.vector_store_repository import VectorStoreRepository
from src.repositories.document_repository import DocumentRepository
from src.config import Config
from src.utils.log_util import Logger
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.schema import Document
from src.utils.vectors_utils import VectorsUtils
from pathlib import Path

class LocalFileRepository(DocumentRepository):
    def __init__(self):
        self.vector_store_repo = VectorStoreRepository()
        self.directory_path = Config.DOCUMENTS_DIRECTORY

    def read_documents(self, directory_path=None):
        """Read documents from the local directory and return a list of document content"""
        if directory_path is None:
            directory_path = self.directory_path
        
        files = self.list_all_files(directory_path)
        Logger.log_info(f"Found {len(files)} files in {directory_path}")
        documents = []
        for file in files:
            document = self.read_file(file, directory_path)
            if document:
                documents.extend(document)
        return documents
    

    def create_embeddings(self):
        """Create or add embeddings to existing"""
        Logger.log_info("Creating embeddings...")
        documents = self.read_documents()
        if documents:
            #vectors_utils = VectorsUtils()
            #embeddings = VectorsUtils().create_embeddings(documents)
            self.save_embeddings(documents)

    def save_embeddings(self, embeddings):
        self.vector_store_repo.add_to_indexes(embeddings)    


    def list_files(self, directory_path=None):
        """List all files in the specified local directory."""
        if directory_path is None:
            directory_path = self.directory_path
        return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    def list_folders(self, directory_path=None):
        """List all folders in the specified local directory."""
        if directory_path is None:
            directory_path = self.directory_path
        return [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]

    def list_all_files(self, directory_path=None, relative_path=""):
        """Recursively list all files in the specified local directory with relative paths."""
        if directory_path is None:
            directory_path = self.directory_path
        
        all_files = []
        files = self.list_files(directory_path)

        # Add files with their relative path
        for file in files:
            all_files.append(os.path.join(relative_path, file))

        folders = self.list_folders(directory_path)

        for folder in folders:
            # Recursively list items in each subfolder
            all_files.extend(self.list_all_files(os.path.join(directory_path, folder), os.path.join(relative_path, folder)))

        return all_files

    def read_file(self, filename, directory_path):
        """Read a single file from the local directory."""
        file_path= Path(directory_path)/filename
        if not os.path.exists(file_path):
            Logger.log_error(f"File does not exist: {file_path}")
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        file_path = os.path.join(directory_path, filename)
        Logger.log_info(f"Reading file: {file_path}")
        if filename.endswith('.txt'):
            loader = TextLoader(file_path)
        elif filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif filename.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        if loader:
            return loader.load()
        else:
            return None
    
