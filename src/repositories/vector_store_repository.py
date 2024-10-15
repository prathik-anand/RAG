import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.config import Config
from src.constants import VECTOR_STORE_SIMILARITY_K

class VectorStoreRepository:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=Config.OPENAI_API_KEY)
        self.persist_directory = Config.VECTOR_STORE_PATH

    """This method will get vectors, if they exist, or create a new vector store"""
    def get_or_create_vector_store(self, texts=None):
        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            print("Loading existing vector store...")
            return Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        else:
            print("Creating new vector store...")
            if texts is None:
                raise ValueError("Texts must be provided to create a new vector store.")
            # Encode documents and save as vectors
            return Chroma.from_documents(texts, self.embeddings, persist_directory=self.persist_directory)

    """This method will perform a similarity search on the vector store"""
    def similarity_search(self, query):
        vector_store = self.get_or_create_vector_store()
        encoded_query = self.embeddings.embed_query(query)
        return vector_store.similarity_search_by_vector(encoded_query, k=VECTOR_STORE_SIMILARITY_K)
