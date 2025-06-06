import pytest
import random
import json
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base, get_db
from app.core.security import verify_password
from unittest.mock import patch

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create a test engine and session factory
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def client():
    """Create a test client for the Flask application and set up an in-memory database."""
    # Create the database tables in the in-memory database
    Base.metadata.create_all(bind=engine)

    app.config['TESTING'] = True

    # Override the get_db dependency to use the testing session
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    # Patch get_db to return the testing session. Use patch as a context manager.
    with patch('app.db.session.get_db', new=override_get_db):
        with app.app_context(): # Push an application context
            with app.test_client() as client:
                yield client

    # Drop the database tables after the test
    Base.metadata.drop_all(bind=engine)


class TestUserRegistration:
    def test_user_registration_success(self, client):
        """Test successful user registration with valid data."""
        user_data = {
            "email": f"test{random.randint(1, 1000000)}@example.com",
            "password": "securepassword123",
            "name": "Test User"
        }
        
        response = client.post(
            '/api/v1/auth/register',
            json=user_data
        )
        
        # Print response details if the assertion fails
        if response.status_code != 201:
            print(f"Registration failed: Status Code - {response.status_code}")
            print(f"Response Data - {response.data}")
            
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['email'] == user_data['email']
        assert response_data['name'] == user_data['name']
        assert 'password' not in response_data  # Ensure password is not returned
        assert 'id' in response_data

    def test_user_registration_invalid_email(self, client):
        """Test user registration with invalid email format."""
        user_data = {
            "email": "invalid-email",
            "password": "securepassword123",
            "name": "Test User"
        }
        
        response = client.post(
            '/api/v1/auth/register',
            json=user_data
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data
        assert 'email' in response_data['error'].lower()

    def test_user_registration_missing_fields(self, client):
        """Test user registration with missing required fields."""
        user_data = {
            "email": "test@example.com"
            # Missing password and name
        }
        
        response = client.post(
            '/api/v1/auth/register',
            json=user_data
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data

    def test_user_registration_duplicate_email(self, client):
        """Test user registration with duplicate email."""
        user_data = {
            "email": f"duplicate{random.randint(0,999999)}@example.com",
            "password": "securepassword123",
            "name": "Test User"
        }
        
        # First registration should succeed
        response1 = client.post(
            '/api/v1/auth/register',
            json=user_data
        )
        assert response1.status_code == 201
        
        # Second registration with same email should fail
        response2 = client.post(
            '/api/v1/auth/register',
            json=user_data
        )
        assert response2.status_code == 400
        response_data = json.loads(response2.data)
        assert 'error' in response_data
        assert 'email' in response_data['error'].lower() or 'exists' in response_data['error'].lower() 


class TestUserLogin:
    def test_user_login_success(self, client):
        """Test successful user login with valid credentials."""
        # First, register a user
        email_address = f"login_test{random.randint(0,999999)}@example.com"
        register_data = {
            "email": email_address,
            "password": "loginpassword123",
            "name": "Login Test User"
        }
        register_response = client.post(
            '/api/v1/auth/register',
            json=register_data
        )
        assert register_response.status_code == 201

        # Now, attempt to login with the registered user's credentials
        login_data = {
            "email": email_address,
            "password": "loginpassword123"
        }

        login_response = client.post(
            '/api/v1/auth/login',
            json=login_data
        )

        assert login_response.status_code == 200
        response_data = json.loads(login_response.data)
        assert 'message' in response_data
        assert response_data['message'] == 'Login successful!'
        assert 'access_token' in response_data

    def test_user_login_invalid_password(self, client):
        """Test user login with invalid password."""
        # First, register a user
        email_address = f"invalid_pass_test{random.randint(0,999999)}@example.com"
        register_data = {
            "email": email_address,
            "password": "validpassword123",
            "name": "Invalid Pass Test User"
        }
        register_response = client.post(
            '/api/v1/auth/register',
            json=register_data
        )
        assert register_response.status_code == 201

        # Now, attempt to login with wrong password
        login_data = {
            "email": email_address,
            "password": "wrongpassword"
        }

        login_response = client.post(
            '/api/v1/auth/login',
            json=login_data
        )

        assert login_response.status_code == 401
        response_data = json.loads(login_response.data)
        assert 'error' in response_data
        assert 'password' in response_data['error'].lower() or 'invalid email or password' in response_data['error'].lower()

    def test_user_login_nonexistent_email(self, client):
        """Test user login with a non-existent email."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "anypassword"
        }

        login_response = client.post(
            '/api/v1/auth/login',
            json=login_data
        )

        assert login_response.status_code == 401
        response_data = json.loads(login_response.data)
        assert 'error' in response_data
        assert 'email' in response_data['error'].lower() or 'invalid email or password' in response_data['error'].lower()

    def test_user_login_missing_fields(self, client):
        """Test user login with missing required fields."""
        login_data = {
            "email": "missing@example.com"
            # Missing password
        }

        login_response = client.post(
            '/api/v1/auth/login',
            json=login_data
        )

        assert login_response.status_code == 400
        response_data = json.loads(login_response.data)
        assert 'error' in response_data 


class TestProtectedRoutes:
    def test_protected_route_no_token(self, client):
        """Test accessing a protected route without a JWT."""
        response = client.get('/api/test')
        assert response.status_code == 401

    def test_protected_route_with_token(self, client):
        """Test accessing a protected route with a valid JWT."""
        # First, register and login a user to get a token
        email_address = f"protected_test{random.randint(0,999999)}@example.com"
        register_data = {
            "email": email_address,
            "password": "protectedpassword",
            "name": "Protected Test User"
        }
        register_response = client.post(
            '/api/v1/auth/register',
            json=register_data
        )
        assert register_response.status_code == 201

        login_data = {
            "email": email_address,
            "password": "protectedpassword"
        }
        login_response = client.post(
            '/api/v1/auth/login',
            json=login_data
        )
        assert login_response.status_code == 200
        access_token = json.loads(login_response.data)['access_token']

        # Access the protected route with the token
        headers = {'Authorization': f'Bearer {access_token}'}
        protected_response = client.get('/api/test', headers=headers)

        # Add this block to print response details if the assertion fails
        if protected_response.status_code != 200:
            print(f"Protected route access failed: Status Code - {protected_response.status_code}")
            try:
                print(f"Response Data - {json.loads(protected_response.data)}")
            except json.JSONDecodeError:
                print(f"Response Data - {protected_response.data}") # Print raw data if not JSON

        assert protected_response.status_code == 200
        response_data = json.loads(protected_response.data)
        assert 'message' in response_data
        assert response_data['message'] == 'Test route works!'
        assert 'current_user' in response_data
        # Optionally, verify the user ID in the response matches the registered user's ID
        # You would need to get the user ID from the register_response if you want to assert this.
        # For simplicity, we are just checking that a current_user is returned. 