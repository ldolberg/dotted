import flask
# from flask import Flask
from app.routes import api_bp
from app.api.v1 import api_v1

app = flask.Flask(__name__)

@app.route("/")
def read_root():
    return {"Hello": "World"}

app.register_blueprint(api_bp)
app.register_blueprint(api_v1)

# TODO: Include blueprints for API endpoints 