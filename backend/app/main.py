import flask
# from flask import Flask
from app.routes import api_bp

app = flask.Flask(__name__)

@app.route("/")
def read_root():
    return {"Hello": "World"}

app.register_blueprint(api_bp)

# TODO: Include blueprints for API endpoints 