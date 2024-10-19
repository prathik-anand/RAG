from flask import request, jsonify, Blueprint
from src.services.rag_service import RAGService

query_bp = Blueprint('query', __name__)
rag_service = RAGService()

@query_bp.route('/query', methods=['POST'])
def query():
    """This endpoint is used to query the Chroma DB"""
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400
    
    query = data['query']
    try:
        response = rag_service.query(query)
        return jsonify({"answer": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


