# User endpoints (Auth, etc.)

# TODO: Implement user authentication and OAuth/Google login 

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity
from app.core.auth import token_required
from app.db.session import get_db
from app.crud.user import get_user_by_email
import json

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/me', methods=['GET'])
@token_required()
def get_current_user():
    """Get current user information based on JWT token."""
    try:
        # Get user identity from JWT token
        current_user_id = get_jwt_identity()
        
        # Get database session
        db = next(get_db())
        try:
            # Find user by ID (the JWT identity is the user ID as string)
            from app.db.models import User
            user = db.query(User).filter_by(id=int(current_user_id)).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Parse roles from JSON string
            try:
                user_roles = json.loads(user.roles) if user.roles else []
            except (json.JSONDecodeError, TypeError):
                user_roles = []
            
            # Return user information (without password)
            user_data = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'roles': user_roles,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
            
            return jsonify(user_data), 200
            
        finally:
            db.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500 