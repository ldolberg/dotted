import pytest
from datetime import date, datetime
import uuid

# Import the Flask app instance
from app.main import app

# Import the db instance
from app.extensions import db # Import db from extensions

# Import your models
from app.db.models import Patient, CommunicationPreference

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
        # Use the existing db instance and create tables
        # db is already initialized with the app in app.main
        db.create_all()

        yield app # provide the app for testing

        # Drop all tables after the module tests are done
        db.drop_all()

    # Restore original database URI after tests
    if original_database_uri is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = original_database_uri

@pytest.fixture(scope='function')
def session(test_app):
    # Provide a database session with transaction management for each test
    with test_app.app_context():
        # Use test_request_context to make db.session available and manage its lifecycle
        with test_app.test_request_context():
            # Begin a transaction or savepoint for rollback
            connection = db.engine.connect()
            transaction = connection.begin()
            
            # Bind the session to this connection for the test
            db.session.configure(bind=connection)

            yield db.session # Provide the session for testing

            # Rollback the transaction and close resources
            transaction.rollback()
            connection.close()
            db.session.remove() # Clean up the session


def test_create_patient(session):
    # Basic test to create a patient and check if it's in the database
    new_patient = Patient(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 5, 15),
        email="john.doe@example.com",
        phone_number="123-456-7890",
        address_street="123 Main St",
        address_city="Anytown",
        address_state="CA",
        address_zip="12345"
    )
    session.add(new_patient)
    session.commit()

    retrieved_patient = session.query(Patient).filter_by(email="john.doe@example.com").first()

    assert retrieved_patient is not None
    assert retrieved_patient.first_name == "John"
    assert retrieved_patient.last_name == "Doe"
    assert retrieved_patient.email == "john.doe@example.com"

    # Example of creating a CommunicationPreference for the patient
    new_preference = CommunicationPreference(
        patient=retrieved_patient, # Link to the patient
        preferred_method="EMAIL",
        allows_appointment_reminders=True,
        allows_billing_notifications=False,
        allows_marketing_updates=False
    )
    session.add(new_preference)
    session.commit()

    # Refresh the patient object to load the relationship
    session.refresh(retrieved_patient)

    assert retrieved_patient.communication_preference is not None
    assert retrieved_patient.communication_preference.preferred_method == "EMAIL"
    assert retrieved_patient.communication_preference.allows_appointment_reminders is True
    assert retrieved_patient.communication_preference.allows_billing_notifications is False
    assert retrieved_patient.communication_preference.allows_marketing_updates is False 