import os
from typing import List
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.utils.log_util import Logger

def read_text_documents(directory_path: str) -> List[Document]:
    Logger.log_info("Reading text documents from directory: " + directory_path)
    documents = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.txt'):
            loader = TextLoader(file_path)
        elif filename.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif filename.endswith('.docx'):
            loader = Docx2txtLoader(file_path)
        else:
            continue  # Skip unsupported file types
        documents.extend(loader.load())
        
    Logger.log_info("Loaded " + str(len(documents)) + " documents")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)
