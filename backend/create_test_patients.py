#!/usr/bin/env python3
"""Create test patients for development and e2e testing."""

from app.db.session import get_db
from app.db.models import Patient, CommunicationPreference
from app.extensions import db
from datetime import date
import uuid

def create_test_patients():
    """Create test patients."""
    try:
        # Create test patients that match what the e2e tests expect
        patients_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'date_of_birth': date(1993, 1, 1),  # This will make age 30 (approximately)
                'email': 'john.doe@example.com',
                'phone_number': '123-456-7890',
                'address_street': '123 Main St',
                'address_city': 'Anytown',
                'address_state': 'CA',
                'address_zip': '12345'
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'date_of_birth': date(1998, 1, 1),  # This will make age 25 (approximately)
                'email': 'jane.smith@example.com',
                'phone_number': '123-456-7890',
                'address_street': '456 Oak Ave',
                'address_city': 'Somewhere',
                'address_state': 'NY',
                'address_zip': '67890'
            },
            {
                'first_name': 'Bob',
                'last_name': 'Johnson',
                'date_of_birth': date(1978, 1, 1),  # This will make age 45 (approximately)
                'email': 'bob.johnson@example.com',
                'phone_number': '555-123-4567',
                'address_street': '789 Pine St',
                'address_city': 'Elsewhere',
                'address_state': 'TX',
                'address_zip': '54321'
            }
        ]

        for patient_data in patients_data:
            # Check if patient already exists
            existing_patient = db.session.query(Patient).filter_by(
                email=patient_data['email'], 
                deleted_at=None
            ).first()
            
            if existing_patient:
                print(f'Patient {patient_data["email"]} already exists')
                continue
                
            # Create new patient
            patient = Patient(**patient_data)
            db.session.add(patient)
            
            # Create communication preference for each patient
            comm_pref = CommunicationPreference(
                patient=patient,
                preferred_method='EMAIL',
                allows_appointment_reminders=True,
                allows_billing_notifications=True,
                allows_marketing_updates=False
            )
            db.session.add(comm_pref)
            
            print(f'Created patient: {patient_data["first_name"]} {patient_data["last_name"]}')

        db.session.commit()
        print('All test patients created successfully')
        
    except Exception as e:
        print(f'Error creating test patients: {e}')
        db.session.rollback()
        raise e

if __name__ == '__main__':
    # Import app directly
    from app.main import app
    
    with app.app_context():
        create_test_patients() 