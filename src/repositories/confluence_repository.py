import os
from atlassian import Confluence
from src.repositories.document_repository import DocumentRepository
from src.repositories.vector_store_repository import VectorStoreRepository
from langchain.schema import Document
from src.utils.log_util import Logger

class ConfluenceRepository(DocumentRepository):
    def __init__(self):
        self.confluence_url = os.getenv('CONFLUENCE_URL')
        self.username = os.getenv('CONFLUENCE_USERNAME')
        self.api_token = os.getenv('CONFLUENCE_API_TOKEN')
        self.space_key = os.getenv('CONFLUENCE_SPACE_KEY')
        
        self.confluence = Confluence(
            url=self.confluence_url,
            username=self.username,
            password=self.api_token
        )
        Logger.info(f"Initialized Confluence Repository with URL: {self.confluence_url}")
        self.vector_store_repo = VectorStoreRepository()

    def read_documents(self):
        """Read documents from Confluence."""
        documents = []
        pages = self.confluence.get_all_pages_from_space(self.space_key)

        for page in pages:
            page_id = page['id']
            page_title = page['title']
            page_content = self.confluence.get_page_by_id(page_id, expand='body.storage')['body']['storage']['value']
            documents.append(Document(page_content=page_content, metadata={"title": page_title}))

        return documents

    def read_files_and_create_embeddings(self):
        """Create embeddings for the provided documents."""
        documents = self.read_documents()
        if documents:
            self.vector_store_repo.add_to_indexes(documents)

    def save_embeddings(self):
        """Save the created embeddings to the vector store."""
        # This can be implemented based on how you want to manage saving
        pass

    def read_all_documents(self):
        """Read documents from a single Confluence space specified by an environment variable."""
        documents = []
        space_key = os.getenv('CONFLUENCE_SPACE_KEY')  # Fetch the space key from environment variable

        if not space_key:
            Logger.error("No space key found in environment variables.")
            return documents  # Return empty if the space key is not set

        Logger.info(f"Reading documents from space: {space_key}")
        pages = self.confluence.get_all_pages_from_space(space_key)

        for page in pages:
            page_id = page['id']
            page_title = page['title']
            page_content = self.confluence.get_page_by_id(page_id, expand='body.storage')['body']['storage']['value']
            documents.append(Document(page_content=page_content, metadata={"title": page_title, "space": space_key}))

        return documents
    
    def create_embeddings(self):
        pass    
