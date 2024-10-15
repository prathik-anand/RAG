from flask import Flask
from flask_cors import CORS
from src.api.query_api import query_bp
from src.config import Config
from src.services.rag_service import RAGService

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Initialize RAGService when the app starts
    RAGService()

    # Register the blueprint
    app.register_blueprint(query_bp)

    return app
