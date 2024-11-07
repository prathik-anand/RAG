import requests
from flask import request, g
from functools import wraps
from src.utils.log_util import Logger
import os

AUTH_SERVER_URL = os.getenv("AUTH_SERVER_URL")  # Base URL for the auth server
AUTH_PROFILE_ENDPOINT = "/auth/profile"  # Endpoint to get user profile

def authorize_request(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            Logger.warning("Authorization token is missing.")
            return {"error": "Authorization token is required."}, 401  # Unauthorized

        # Validate the token and retrieve the user profile from the auth server
        try:
            # Log the URL for debugging
            Logger.info(f"Using AUTH_SERVER_URL: {AUTH_SERVER_URL}")

            # Make a request to the auth server to get the user profile
            response = requests.get(f"{AUTH_SERVER_URL}{AUTH_PROFILE_ENDPOINT}", headers={"Authorization": token})
            if response.status_code != 200:
                Logger.warning("Invalid authorization token.")
                return {"error": "Invalid authorization token."}, 403  # Forbidden

            g.user_profile = response.json() 
            Logger.info("User profile retrieved successfully.")
        except Exception as e:
            Logger.error(f"Error validating token: {str(e)}")
            return {"error": "Error validating token."}, 500  # Internal Server Error

        return f(*args, **kwargs)

    return decorated_function 