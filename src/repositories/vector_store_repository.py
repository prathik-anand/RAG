import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.config import Config
from src.utils.log_util import Logger
from src.utils.vectors_utils import VectorsUtils
import shutil
from src.constants import VECTOR_STORE_SIMILARITY_K

class VectorStoreRepository:
    def __init__(self):
        Logger.log_info("Initializing VectorStoreRepository...")
        self.embeddings = OpenAIEmbeddings(api_key=Config.OPENAI_API_KEY)
        self.persist_directory = Config.VECTOR_STORE_PATH
        
        self.vector_store = self.initialize_vector_store()

    def initialize_vector_store(self):
        """Initialize the vector store."""
        if self.is_vector_store_exists():
            Logger.log_info("Loading existing vector store...")
            return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        else:
            Logger.log_info("Vector store does not exist.")
            return None  # This will be handled in VectorStoreManager

    def is_vector_store_exists(self):
        return os.path.exists(self.persist_directory) and os.listdir(self.persist_directory)

    def similarity_search(self, query):
        """This method will perform a similarity search on the vector store"""
        encoded_query = self.embeddings.embed_query(query)
        return self.vector_store.similarity_search_by_vector(encoded_query, k=VECTOR_STORE_SIMILARITY_K)
    
    def add_to_indexes(self, texts):
        try:
            """This method is used to add document for existing indexes"""
            Logger.log_info("Creating partial indexes...")
            if not texts:
                Logger.log_error("Texts must be provided to add to indexes.")
                raise ValueError("Texts must be provided to add to indexes.")
            
            chunked_docs = VectorsUtils.create_chunked_documents(texts)
            self.vector_store.add_documents(chunked_docs)
            
        except Exception as e:
            Logger.log_error(f"Error adding texts to vector store: {e}")
            raise e
        
    def delete_indexes(self):
        """This is used to delete the existing vectorstore"""
        Logger.log_info("Deleting indexes...")
        shutil.rmtree(self.persist_directory)