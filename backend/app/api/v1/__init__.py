from flask import Blueprint
from .endpoints.auth import auth_bp

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Register auth endpoints
api_v1.register_blueprint(auth_bp, url_prefix='/auth') 