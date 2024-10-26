import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.config import Config
from src.constants import VECTOR_STORE_SIMILARITY_K
import shutil
from src.utils.log_util import Logger

class VectorStoreRepository:
    def __init__(self):
        Logger.log_info("Initializing VectorStoreRepository...")    
        self.embeddings = OpenAIEmbeddings(api_key=Config.OPENAI_API_KEY)
        self.persist_directory = Config.VECTOR_STORE_PATH

    def get_or_create_vector_store(self, texts=None):
        """This method will get vectors, if they exist, or create a new vector store"""
        if self.is_vector_store_exists():
            Logger.log_info("Loading existing vector store...")
            return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        else:
            if texts is None:
                Logger.log_error("Texts must be provided to create a new vector store.")
                raise ValueError("Texts must be provided to create a new vector store.")
            # Encode documents and save as vectors
            return self.create_full_indexes(texts)

    
    def similarity_search(self, query):
        """This method will perform a similarity search on the vector store"""
        vector_store = self.get_or_create_vector_store()
        encoded_query = self.embeddings.embed_query(query)
        return vector_store.similarity_search_by_vector(encoded_query, k=VECTOR_STORE_SIMILARITY_K)

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
            #self.delete_indexes()
        
        Logger.log_info("Creating new vector store...")
        return Chroma.from_documents(texts, self.embeddings, persist_directory=self.persist_directory)
        
    def add_to_indexes(self, texts):
        """This method is used to add document for existing indexes"""
        Logger.log_info("Creating partial indexes...")
        if not texts:
            Logger.log_error("Texts must be provided to add to indexes.")
            raise ValueError("Texts must be provided to add to indexes.")
        
        if self.is_vector_store_exists():   
            #Chroma.add_documents(texts, self.embeddings, persist_directory=self.persist_directory)
            pass
        else:
            self.create_full_indexes(texts)
        
    def delete_indexes(self):
        """This is used to delete the existing vectorstore"""
        Logger.log_info("Deleting indexes...")
        shutil.rmtree(self.persist_directory)
