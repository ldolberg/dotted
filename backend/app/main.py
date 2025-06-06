import flask
# from flask import Flask
from app.routes import api_bp
from app.api.v1 import api_v1
from flask_jwt_extended import JWTManager # Import JWTManager

app = flask.Flask(__name__)

# Configure JWTManager
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in production!
jwt = JWTManager(app)

@app.route("/")
def read_root():
    return {"Hello": "World"}

app.register_blueprint(api_bp)
app.register_blueprint(api_v1)

# TODO: Include blueprints for API endpoints 