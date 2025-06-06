from flask import Blueprint
from .endpoints.auth import auth_bp
from .endpoints.patients import patients_bp

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Register auth endpoints
api_v1.register_blueprint(auth_bp, url_prefix='/auth')

# Register patients endpoints
api_v1.register_blueprint(patients_bp, url_prefix='/patients') 