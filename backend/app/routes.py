from flask import Blueprint, jsonify # Import jsonify
from app.api.v1.endpoints.auth import auth_bp # Import the auth blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity # Import jwt_required and get_jwt_identity

# Create a Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Define a simple route within the blueprint
@api_bp.route('/test')
@jwt_required() # Add this decorator to protect the route
def test_route():
    current_user_id = get_jwt_identity() # Get the user's identity from the token
    return jsonify({"message": "Test route works!", "current_user": current_user_id})

# Register the authentication blueprint
api_bp.register_blueprint(auth_bp, url_prefix='/v1')

# You can define more routes here 