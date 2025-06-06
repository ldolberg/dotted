import re
from flask import Blueprint, request, jsonify
from app.db.session import SessionLocal
from app.crud.user import get_user_by_email, create_user
from app.db import create_tables

auth_bp = Blueprint('auth', __name__)

# Initialize tables on first import
try:
    create_tables()
except Exception as e:
    # Log the error but don't fail the import
    print(f"Warning: Could not create tables: {e}")


def is_valid_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'name']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate email format
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Create database session
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = get_user_by_email(db, data['email'])
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = create_user(
            db=db,
            email=data['email'],
            name=data['name'],
            password=data['password']
        )
        
        response_data = {
            'id': user.id,
            'email': user.email,
            'name': user.name
        }
        
        return jsonify(response_data), 201
        
    finally:
        db.close() 