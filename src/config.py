import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DOCUMENTS_DIRECTORY = os.getenv("DOCUMENTS_DIRECTORY", "./data")
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
    
    # Google Drive Configuration
    GOOGLE_DRIVE_CREDENTIALS_FILE = os.getenv("GOOGLE_DRIVE_CREDENTIALS_FILE", "./credentials.json")
