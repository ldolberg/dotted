from flask import Blueprint

# Create a Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Define a simple route within the blueprint
@api_bp.route('/test')
def test_route():
    return {"message": "Test route works!"}

# You can define more routes here 