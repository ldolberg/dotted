import pytest
import json
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestUserRegistration:
    def test_user_registration_success(self, client):
        """Test successful user registration with valid data."""
        user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "name": "Test User"
        }
        
        response = client.post(
            '/api/v1/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
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
            data=json.dumps(user_data),
            content_type='application/json'
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
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert 'error' in response_data

    def test_user_registration_duplicate_email(self, client):
        """Test user registration with duplicate email."""
        user_data = {
            "email": "duplicate@example.com",
            "password": "securepassword123",
            "name": "Test User"
        }
        
        # First registration should succeed
        response1 = client.post(
            '/api/v1/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        assert response1.status_code == 201
        
        # Second registration with same email should fail
        response2 = client.post(
            '/api/v1/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        assert response2.status_code == 400
        response_data = json.loads(response2.data)
        assert 'error' in response_data
        assert 'email' in response_data['error'].lower() or 'exists' in response_data['error'].lower() 