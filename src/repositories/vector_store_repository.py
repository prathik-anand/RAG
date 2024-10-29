import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.config import Config
from src.constants import VECTOR_STORE_SIMILARITY_K
import shutil
from src.utils.log_util import Logger
from src.utils.vectors_utils import VectorsUtils
from src.utils.document_processor import read_text_documents

class VectorStoreRepository:
    def __init__(self):
        Logger.log_info("Initializing VectorStoreRepository...")    
        self.embeddings = OpenAIEmbeddings(api_key=Config.OPENAI_API_KEY)
        self.persist_directory = Config.VECTOR_STORE_PATH
        
        # Initialize Chroma directly in the constructor
        if self.is_vector_store_exists():
            Logger.log_info("Loading existing vector store...")
            self.vector_store = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        else:
            Logger.log_info("Creating new vector store...")
            documents = self.read_documents()
            if not documents:
                Logger.log_error("No documents found to create a new vector store.")
                raise ValueError("No documents found to create a new vector store.")
            self.vector_store = Chroma.from_documents(documents, self.embeddings, persist_directory=self.persist_directory)

    def read_documents(self):
        """Read documents from the source (e.g., local files or other sources)."""
        directory_path = Config.DOCUMENTS_DIRECTORY
        return read_text_documents(directory_path)

    def similarity_search(self, query):
        """This method will perform a similarity search on the vector store"""
        encoded_query = self.embeddings.embed_query(query)
        return self.vector_store.similarity_search_by_vector(encoded_query, k=VECTOR_STORE_SIMILARITY_K)

    def is_vector_store_exists(self):
        return os.path.exists(self.persist_directory) and os.listdir(self.persist_directory)
    
    def create_full_indexes(self, texts):
        """This method is used to create indexes from scratch"""
        Logger.log_info("Creating full indexes...")
        if not texts:
            Logger.log_error("Texts must be provided to create a new vector store.")
            raise ValueError("Texts must be provided to create a new vector store.")
        
        if self.is_vector_store_exists():
            Logger.log_info("Deleting existing vector store...")
            self.delete_indexes()
        
        Logger.log_info("Creating new vector store...")
        self.vector_store = Chroma.from_documents(texts, self.embeddings, persist_directory=self.persist_directory)
        return self.vector_store
        
    def add_to_indexes(self, texts):
        try:
            """This method is used to add document for existing indexes"""
            Logger.log_info("Creating partial indexes...")
            if not texts:
                Logger.log_error("Texts must be provided to add to indexes.")
                raise ValueError("Texts must be provided to add to indexes.")
        
            if self.is_vector_store_exists():   
                embeddingss = VectorsUtils.create_embeddings(texts)
                self.vector_store.add_documents(embeddingss)
            else:
                self.create_full_indexes(texts)
        except Exception as e:
            Logger.log_error(f"Error adding texts to vector store: {e}")
            raise e
        
    def delete_indexes(self):
        """This is used to delete the existing vectorstore"""
        Logger.log_info("Deleting indexes...")
        shutil.rmtree(self.persist_directory)
