import re
import json
from flask import Blueprint, request, jsonify, redirect, url_for, session
from app.db.session import get_db
from app.crud.user import get_user_by_email, create_user
from app.db import create_tables
from flask_jwt_extended import create_access_token
from requests_oauthlib.oauth2_session import OAuth2Session
import os

# TODO: Load environment variables for Google OAuth credentials and redirect URI
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

# Google OAuth URLs
GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

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
    
    # Create database session using get_db
    db = next(get_db())
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


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.get_json()

    # Validate required fields
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    db = next(get_db())
    try:
        # Check if user exists and password is correct
        user = get_user_by_email(db, data['email'])
        if user and user.check_password(data['password']):
            # Create the access token for the user with roles
            try:
                user_roles = json.loads(user.roles) if user.roles else []
            except (json.JSONDecodeError, TypeError):
                user_roles = []
            additional_claims = {"roles": user_roles}
            access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
            return jsonify({'message': 'Login successful!', 'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    finally:
        db.close()


@auth_bp.route('/google-login')
def google_login():
    """Initiate Google OAuth login flow."""
    if not GOOGLE_CLIENT_ID or not GOOGLE_REDIRECT_URI:
        return jsonify({'error': 'Google OAuth credentials not configured.'}), 500

    # Define the scopes needed
    scopes = [
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ]

    # Create an OAuth2 session
    google = OAuth2Session(GOOGLE_CLIENT_ID, scope=scopes, redirect_uri=GOOGLE_REDIRECT_URI)

    # Get the authorization URL and state
    authorization_url, state = google.authorization_url(GOOGLE_AUTHORIZATION_URL, access_type="offline", prompt="select_account")

    # Store the state in the session to prevent CSRF (requires Flask session configuration)
    # flask.session['oauth_state'] = state # This needs Flask session to be configured
    print(f"OAuth state: {state}") # Log state for now

    return redirect(authorization_url)


@auth_bp.route('/google-callback')
def google_callback():
    """Handle the callback from Google OAuth."""
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET or not GOOGLE_REDIRECT_URI:
        return jsonify({'error': 'Google OAuth credentials not configured.'}), 500

    # Retrieve the state from the session (requires Flask session configuration)
    # state = flask.session.pop('oauth_state', None) # Use this when Flask session is configured
    state = request.args.get('state') # For now, get state from args (less secure)

    # Check if the state is valid (CSRF protection)
    # if state is None or state != request.args.get('state'): # Use this when Flask session is configured
    #    return jsonify({'error': 'Invalid state parameter.'}), 400
    # For now, we proceed without state validation for simplicity, but it's crucial for security.
    print(f"Received state: {state}") # Log received state

    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=GOOGLE_REDIRECT_URI, state=state)

    try:
        # Fetch the access token
        token = google.fetch_token(GOOGLE_TOKEN_URL,
                                 client_secret=GOOGLE_CLIENT_SECRET,
                                 authorization_response=request.url)

        # Fetch user info
        userinfo = google.get(GOOGLE_USERINFO_URL).json()

        user_email = userinfo.get('email')
        user_name = userinfo.get('name')

        if not user_email:
            return jsonify({'error': 'Could not retrieve email from Google.'}), 500

        db = next(get_db())
        try:
            # Check if user exists
            user = get_user_by_email(db, user_email)

            if user:
                # Existing user, generate JWT with roles
                try:
                    user_roles = json.loads(user.roles) if user.roles else []
                except (json.JSONDecodeError, TypeError):
                    user_roles = []
                additional_claims = {"roles": user_roles}
                access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)
                return jsonify({'message': 'Login successful!', 'access_token': access_token}), 200
            else:
                # New user, create in database and generate JWT
                # For simplicity, generating a random password. In a real app, handle this securely or mark as OAuth user.
                # You might also want to redirect the user to a profile completion page.
                new_user = create_user(db=db, email=user_email, name=user_name or user_email, password=os.urandom(16).hex())
                try:
                    new_user_roles = json.loads(new_user.roles) if new_user.roles else []
                except (json.JSONDecodeError, TypeError):
                    new_user_roles = []
                additional_claims = {"roles": new_user_roles}
                access_token = create_access_token(identity=str(new_user.id), additional_claims=additional_claims)
                return jsonify({'message': 'User created and logged in successfully!', 'access_token': access_token}), 201

        finally:
            db.close()

    except Exception as e:
        print(f"Error during Google OAuth callback: {e}")
        return jsonify({'error': 'Failed to process Google login.', 'details': str(e)}), 500 