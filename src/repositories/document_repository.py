from abc import ABC, abstractmethod
from langchain.schema import Document
from typing import List

class DocumentRepository(ABC):
    @abstractmethod
    def read_documents(self):
        """Read documents from the source and return a list of Document objects."""
        pass

    @abstractmethod
    def create_embeddings(self, documents):
        """Create embeddings for the provided documents."""
        pass
