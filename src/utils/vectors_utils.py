from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
class VectorsUtils:
    def __init__(self):
        pass
    
    @staticmethod
    def create_embeddings(documents_content):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(documents_content)