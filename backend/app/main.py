import flask
# from flask import Flask
from app.routes import api_bp
from app.api.v1 import api_v1
from flask_jwt_extended import JWTManager # Import JWTManager
from app.extensions import db, migrate # Import db and migrate from extensions

app = flask.Flask(__name__)

# Configure JWTManager
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in production!
jwt = JWTManager(app)

# Database Configuration (example - adjust with your actual config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/app_db' # Use your database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-SQLAlchemy and Flask-Migrate with the app
db.init_app(app)
migrate.init_app(app, db)

@app.route("/")
def read_root():
    return {"Hello": "World"}

app.register_blueprint(api_bp)
app.register_blueprint(api_v1)

# TODO: Include blueprints for API endpoints 