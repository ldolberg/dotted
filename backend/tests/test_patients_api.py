import pytest
import json
import random
from datetime import date, datetime, timezone
import uuid
from flask_jwt_extended import create_access_token # Import create_access_token
from app.core.security import get_password_hash # Import the password hashing function

# Import the Flask app instance
from app.main import app

# Import the db instance
from app.extensions import db # Import db from extensions

# Import your models
from app.db.models import Patient, CommunicationPreference, User # Import User model

# Use an in-memory SQLite database for testing
TEST_DATABASE_URI = "sqlite:///:memory:"

@pytest.fixture(scope='module')
def test_app():
    # Configure the Flask app for testing
    # Temporarily store original config to restore later
    original_database_uri = app.config.get('SQLALCHEMY_DATABASE_URI')

    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recommended for Flask-SQLAlchemy

    # Push an application context
    with app.app_context():
        # Initialize db with the test app (if not already initialized)
        # A safer approach might be to check if app.extensions['sqlalchemy'] exists before init_app
        if 'sqlalchemy' not in app.extensions:
             db.init_app(app)

        # Create all tables using Flask-SQLAlchemy's db.create_all
        db.create_all()

        yield app # provide the app for testing

        # Drop all tables using Flask-SQLAlchemy's db.drop_all after the module tests are done
        db.drop_all()

    # Restore original database URI after tests
    if original_database_uri is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = original_database_uri


@pytest.fixture(scope='function')
def client(test_app):
    # Provide a test client for making HTTP requests
    with test_app.app_context():
        # Use test_request_context for db.session to work correctly in tests
        with test_app.test_request_context():
            yield test_app.test_client()


@pytest.fixture(scope='function')
def session(test_app):
    # Provide a database session with transaction management for each test
    with test_app.app_context():
        # Use test_request_context to make db.session available and manage its lifecycle
        with test_app.test_request_context():
            # Bind the Flask-SQLAlchemy session to a connection with a transaction
            connection = db.engine.connect()
            transaction = connection.begin()

            # Configure the session to use this connection
            db.session.configure(bind=connection)

            # Use a nested transaction for rollback per test function if needed,
            # but the function-scoped transaction should be sufficient here.
            # db.session.begin_nested()

            yield db.session # Provide the session for testing

            # Rollback the transaction and clean up the session
            transaction.rollback()
            connection.close()
            db.session.remove() # Clean up the session


# Fixture to register and log in a user, returning an access token
@pytest.fixture(scope='function')
def auth_token(session): # Change client to session as we'll interact with the db
    email_address = f"api_test_{random.randint(0, 999999)}@example.com"
    password = "apitestpassword"
    name = "API Test User"
    roles = ["ADMIN"] # Assign ADMIN role

    # Hash the password before creating the user
    hashed_password = get_password_hash(password)

    # Create user directly in the database
    user = User(
        email=email_address,
        name=name,
        hashed_password=hashed_password # Pass the hashed password
    )
    # Assuming User model has a 'roles' attribute (e.g., a JSON or array column, or a relationship)
    # If not, you'll need to add it or simulate role checking differently.
    # For this example, I'll assume a simple way to attach roles for testing.
    # A common way is a 'roles' column storing a list/JSON of strings.
    user.roles = roles # Assign roles to the user object

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate JWT with claims
    # The identity should be something unique for the user, like their ID or email
    # Ensure your JWT setup is configured to process 'roles' claim from identity
    # Pass the locally defined roles list directly to additional_claims
    access_token = create_access_token(identity=str(user.id), additional_claims={"roles": roles})

    # print(f"Generated token for user {user.email} with roles: {user.roles}") # Optional: for debugging

    return access_token


class TestPatientAPI:

    def test_get_all_patients(self, client, auth_token, session): # Added session fixture
        # Test retrieving all patients (should be empty initially)
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get('/api/v1/patients', headers=headers)
        assert response.status_code == 200, headers
        data = json.loads(response.data)
        assert "data" in data
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 0

        # Create a patient to ensure it appears in the list
        patient1 = Patient(
            first_name="PatientOne", last_name="Test", date_of_birth=date(2000, 1, 1),
            email=f"patient1_{random.randint(0, 999999)}@example.com"
        )
        session.add(patient1)
        session.commit()
        session.refresh(patient1)

        response_after_create = client.get('/api/v1/patients', headers=headers)
        assert response_after_create.status_code == 200
        data_after_create = json.loads(response_after_create.data)
        assert len(data_after_create["data"]) == 1
        assert data_after_create["data"][0]["email"] == patient1.email


    def test_create_patient(self, client, auth_token, session):
        # Test creating a new patient
        patient_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "1995-10-20",
            "email": f"jane.doe_{random.randint(0, 999999)}@example.com",
            "phone_number": "987-654-3210",
            "address_street": "456 Oak Ave",
            "address_city": "Othertown",
            "address_state": "NY",
            "address_zip": "67890",
            "communication_preference": {
                "preferred_method": "SMS",
                "allows_appointment_reminders": False,
                "allows_billing_notifications": True,
                "allows_marketing_updates": True
            }
        }
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }

        response = client.post('/api/v1/patients', headers=headers, data=json.dumps(patient_data))

        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert "data" in response_data
        created_patient_data = response_data["data"]

        assert "id" in created_patient_data
        assert created_patient_data["first_name"] == patient_data["first_name"]
        assert created_patient_data["email"] == patient_data["email"]
        assert "communication_preference" in created_patient_data
        assert created_patient_data["communication_preference"]["preferred_method"] == patient_data["communication_preference"]["preferred_method"]

        # Verify in database (optional but good practice)
        created_patient_id = uuid.UUID(created_patient_data["id"])
        patient_in_db = session.query(Patient).filter_by(id=created_patient_id).first()
        assert patient_in_db is not None
        assert patient_in_db.email == patient_data["email"]
        assert patient_in_db.communication_preference is not None
        assert patient_in_db.communication_preference.preferred_method == patient_data["communication_preference"]["preferred_method"]

    def test_get_patient_by_id(self, client, auth_token, session):
        # Test retrieving a patient by ID
        # First, create a patient directly in the database for retrieval
        patient_to_get = Patient(
            first_name="Retrieve",
            last_name="Test",
            date_of_birth=date(1985, 1, 25),
            email=f"retrieve.test_{random.randint(0, 999999)}@example.com",
            phone_number="111-222-3333"
        )
        session.add(patient_to_get)
        session.commit()
        session.refresh(patient_to_get)

        headers = {'Authorization': f'Bearer {auth_token}'}
        response = client.get(f'/api/v1/patients/{patient_to_get.id}', headers=headers)

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert "data" in response_data
        retrieved_patient_data = response_data["data"]

        assert retrieved_patient_data["id"] == str(patient_to_get.id)
        assert retrieved_patient_data["first_name"] == patient_to_get.first_name
        assert retrieved_patient_data["email"] == patient_to_get.email

        # Test retrieving a non-existent patient
        non_existent_id = uuid.uuid4()
        response_non_existent = client.get(f'/api/v1/patients/{non_existent_id}', headers=headers)
        assert response_non_existent.status_code == 404


    def test_update_patient(self, client, auth_token, session):
        # Test updating an existing patient
        # Create a patient first
        patient_to_update = Patient(
            first_name="Update",
            last_name="Test",
            date_of_birth=date(1990, 7, 10),
            email=f"update.test_{random.randint(0, 999999)}@example.com",
            phone_number="555-123-4567"
        )
        session.add(patient_to_update)
        session.commit()
        session.refresh(patient_to_update)

        update_data = {
            "first_name": "Updated",
            "phone_number": "999-888-7777",
            "communication_preference": {
                "preferred_method": "PHONE",
                "allows_marketing_updates": True
            }
        }
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }

        response = client.put(f'/api/v1/patients/{patient_to_update.id}', headers=headers, data=json.dumps(update_data))

        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert "data" in response_data
        updated_patient_data = response_data["data"]

        assert updated_patient_data["id"] == str(patient_to_update.id)
        assert updated_patient_data["first_name"] == update_data["first_name"]
        assert updated_patient_data["phone_number"] == update_data["phone_number"]
        assert updated_patient_data["communication_preference"]["preferred_method"] == update_data["communication_preference"]["preferred_method"]
        assert updated_patient_data["communication_preference"]["allows_marketing_updates"] == update_data["communication_preference"]["allows_marketing_updates"]

        # Verify changes in database
        patient_in_db = session.query(Patient).filter_by(id=patient_to_update.id).first()
        assert patient_in_db.first_name == update_data["first_name"]
        assert patient_in_db.phone_number == update_data["phone_number"]
        assert patient_in_db.communication_preference.preferred_method == update_data["communication_preference"]["preferred_method"]
        assert patient_in_db.communication_preference.allows_marketing_updates == update_data["communication_preference"]["allows_marketing_updates"]


    def test_delete_patient(self, client, auth_token, session):
        # Test soft deleting a patient
        # Create a patient first
        patient_to_delete = Patient(
            first_name="Delete",
            last_name="Test",
            date_of_birth=date(1992, 11, 5),
            email=f"delete.test_{random.randint(0, 999999)}@example.com",
            phone_number="123-987-6540"
        )
        session.add(patient_to_delete)
        session.commit()
        session.refresh(patient_to_delete)
        patient_id = patient_to_delete.id

        headers = {'Authorization': f'Bearer {auth_token}'}
        # Note: DELETE requires 'ADMIN' role according to the blueprint definition.
        # The current auth_token fixture provides a token for a user registered via auth/register,
        # which might not have the 'ADMIN' role. You may need a separate fixture for ADMIN tokens
        # or modify the auth setup to assign roles during registration for testing purposes.
        # For now, this test will likely fail with 403 if the user doesn't have the ADMIN role.
        response = client.delete(f'/api/v1/patients/{patient_id}', headers=headers)

        # If the user doesn't have ADMIN role, expect 403. If they do, expect 204.
        # Assuming for this test that the authenticated user *does* have the ADMIN role or
        # the token_required decorator is bypassed/mocked for testing DELETE.
        # If running with a user that doesn't have ADMIN, the next assert will fail with 403.
        assert response.status_code == 204
        # Verify response body is empty
        assert response.data == b''

        # Verify in database that deleted_at is set
        deleted_patient_in_db = session.query(Patient).filter_by(id=patient_id).first()
        assert deleted_patient_in_db is not None
        assert deleted_patient_in_db.deleted_at is not None
        # Check that deleted_at is a datetime object and is recent
        assert isinstance(deleted_patient_in_db.deleted_at, datetime)
        # Using timezone.utc for comparison as datetime.utcnow() is timezone-naive but recommended
        assert (datetime.now(timezone.utc) - deleted_patient_in_db.deleted_at.replace(tzinfo=timezone.utc)).total_seconds() < 5 # Check if timestamp is recent


        # Verify the patient is not returned in the get all non-deleted patients endpoint
        response_get_all = client.get('/api/v1/patients', headers=headers)
        assert response_get_all.status_code == 200
        data_get_all = json.loads(response_get_all.data)
        assert "data" in data_get_all
        # Check that no patient in the list has the deleted patient's ID
        assert all(item['id'] != str(patient_id) for item in data_get_all['data'])

        # Test retrieving the deleted patient by ID (should be 404)
        response_get_deleted = client.get(f'/api/v1/patients/{patient_id}', headers=headers)
        assert response_get_deleted.status_code == 404
