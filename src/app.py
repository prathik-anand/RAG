from flask import Flask
from flask_cors import CORS
from src.controller.query_controller import query_bp
from src.config import Config
from src.services.vector_store_manager import VectorStoreManager

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for requests from http://localhost:3000
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    
    app.config.from_object(Config)

    # Initialize the vector store when the app starts
    VectorStoreManager.get_vector_store()

    # Register the blueprint
    app.register_blueprint(query_bp)

    return app
