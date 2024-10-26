import os
from atlassian import Confluence
from src.repositories.document_repository import DocumentRepository
from src.repositories.vector_store_repository import VectorStoreRepository

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

    def create_embeddings(self, documents):
        """Create embeddings for the provided documents."""
        if documents:
            self.vector_store_repo.get_or_create_vector_store(documents)

    def save_embeddings(self):
        """Save the created embeddings to the vector store."""
        # This can be implemented based on how you want to manage saving
        pass
