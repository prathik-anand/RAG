from flask import request, jsonify, Blueprint
from src.services.rag_service import RAGService
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

query_bp = Blueprint('query', __name__)
rag_service = RAGService()

@query_bp.route('/query', methods=['POST'])
def query():
    """This endpoint is used to query the Chroma DB"""
    try:
        query_input = request.json.get('query')
        user_id = 1
        chat_id = request.args.get('chat_id')
        if chat_id == '':
            chat_id = None

        ip_address = request.remote_addr
        ip_metadata = requests.get(f'http://ip-api.com/json/{ip_address}')
        # location = ip_metadata.json()['city']
        location = None
        
        title, response = rag_service.get_answer(user_id, query_input, ip_address, location, chat_id)
        
        logger.info(f"Query processed successfully for user_id: {user_id}, chat_id: {chat_id}")
        
        return jsonify({"title": title, "response": response}), 200

    except ValueError as ve:
        logger.warning(f"ValueError: {str(ve)}")
        return jsonify({"error": str(ve)}), 400  # Bad Request
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred: " + str(e)}), 500  # Internal Server Error
