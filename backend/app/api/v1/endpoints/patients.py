from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from datetime import datetime
import uuid

from app.extensions import db
from app.db.models import Patient, CommunicationPreference
from app.core.auth import token_required # Assuming token_required is in app.core.auth

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

# Helper function for patient validation (basic example)
def validate_patient_data(data, is_update=False):
    errors = {}
    if not is_update or 'first_name' in data:
        if not data.get('first_name'):
            errors['first_name'] = 'First name is required.'
    if not is_update or 'last_name' in data:
        if not data.get('last_name'):
            errors['last_name'] = 'Last name is required.'
    if not is_update or 'date_of_birth' in data:
        try:
            datetime.strptime(data.get('date_of_birth', ''), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            errors['date_of_birth'] = 'Valid date of birth (YYYY-MM-DD) is required.'
    if not is_update or 'email' in data:
        if not data.get('email') or '@' not in data.get('email', ''):
             errors['email'] = 'Valid email is required.'
        # Add check for unique email on creation
        if not is_update and data.get('email'):
            existing_patient = db.session.query(Patient).filter_by(email=data['email'], deleted_at=None).first()
            if existing_patient:
                errors['email'] = 'Email address already exists.'

    # Basic validation for communication preference if provided
    comm_pref_data = data.get('communication_preference')
    if comm_pref_data is not None:
        allowed_methods = ['EMAIL', 'SMS', 'PHONE']
        if 'preferred_method' in comm_pref_data and comm_pref_data['preferred_method'] not in allowed_methods:
             errors['communication_preference'] = f'Preferred method must be one of {allowed_methods}.'

    return errors


@patients_bp.route('', methods=['GET'])
@token_required(['ADMIN', 'STAFF'])
def get_all_patients():
    patients = db.session.query(Patient).options(joinedload(Patient.communication_preference)).filter(Patient.deleted_at.is_(None)).all()
    return jsonify({"data": [patient.to_dict() for patient in patients]}), 200

@patients_bp.route('/<uuid:patient_id>', methods=['GET'])
@token_required(['ADMIN', 'STAFF'])
def get_patient(patient_id):
    patient = db.session.query(Patient).options(joinedload(Patient.communication_preference)).filter_by(id=patient_id, deleted_at=None).first_or_404()
    return jsonify({"data": patient.to_dict()}), 200

@patients_bp.route('', methods=['POST'])
@token_required(['ADMIN', 'STAFF'])
def create_patient():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data provided."}), 400

    errors = validate_patient_data(data)
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    # Extract patient data
    patient_data = {
        key: data.get(key) for key in [
            'first_name', 'last_name', 'date_of_birth', 'email', 'phone_number',
            'address_street', 'address_city', 'address_state', 'address_zip'
        ]
    }
    # Convert date_of_birth string to date object
    if patient_data.get('date_of_birth'):
        try:
            patient_data['date_of_birth'] = datetime.strptime(patient_data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
             # Should be caught by validation, but as a safeguard
             return jsonify({"error": "Invalid date format for date_of_birth. Use YYYY-MM-DD."}), 400

    new_patient = Patient(**patient_data)

    # Handle communication preference if provided
    comm_pref_data = data.get('communication_preference')
    if comm_pref_data is not None:
         # Validation for communication preference already done in validate_patient_data
         new_preference = CommunicationPreference(
             patient=new_patient, # Link to the patient
             preferred_method=comm_pref_data.get('preferred_method', 'EMAIL'),
             allows_appointment_reminders=comm_pref_data.get('allows_appointment_reminders', True),
             allows_billing_notifications=comm_pref_data.get('allows_billing_notifications', True),
             allows_marketing_updates=comm_pref_data.get('allows_marketing_updates', False)
         )
         db.session.add(new_preference)

    db.session.add(new_patient)
    db.session.commit()

    # Refresh to get the communication preference relationship loaded if added
    db.session.refresh(new_patient)

    return jsonify({"data": new_patient.to_dict()}), 201

@patients_bp.route('/<uuid:patient_id>', methods=['PUT'])
@token_required(['ADMIN', 'STAFF'])
def update_patient(patient_id):
    patient = db.session.query(Patient).filter_by(id=patient_id, deleted_at=None).first_or_404()
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data provided."}), 400

    errors = validate_patient_data(data, is_update=True)
    if errors:
         return jsonify({"error": "Validation failed", "details": errors}), 400

    # Update patient fields
    for field in ['first_name', 'last_name', 'email', 'phone_number', 'address_street', 'address_city', 'address_state', 'address_zip']:
        if field in data:
            setattr(patient, field, data[field])
            
    # Update date_of_birth if provided
    if 'date_of_birth' in data:
        try:
            patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
             return jsonify({"error": "Invalid date format for date_of_birth. Use YYYY-MM-DD."}), 400

    # Update communication preference if provided
    comm_pref_data = data.get('communication_preference')
    if comm_pref_data is not None:
        if patient.communication_preference:
             # Update existing preference
             for field in ['preferred_method', 'allows_appointment_reminders', 'allows_billing_notifications', 'allows_marketing_updates']:
                  if field in comm_pref_data:
                       setattr(patient.communication_preference, field, comm_pref_data[field])
        else:
             # Create new preference if it doesn't exist
             new_preference = CommunicationPreference(
                 patient=patient,
                 preferred_method=comm_pref_data.get('preferred_method', 'EMAIL'),
                 allows_appointment_reminders=comm_pref_data.get('allows_appointment_reminders', True),
                 allows_billing_notifications=comm_pref_data.get('allows_billing_notifications', True),
                 allows_marketing_updates=comm_pref_data.get('allows_marketing_updates', False)
             )
             db.session.add(new_preference)

    # Update updated_at timestamp
    patient.updated_at = datetime.utcnow()

    db.session.commit()
    db.session.refresh(patient)

    return jsonify({"data": patient.to_dict()}), 200

@patients_bp.route('/<uuid:patient_id>', methods=['DELETE'])
@token_required(['ADMIN'])
def delete_patient(patient_id):
    patient = db.session.query(Patient).filter_by(id=patient_id, deleted_at=None).first_or_404()

    # Soft delete by setting deleted_at timestamp
    patient.deleted_at = datetime.utcnow()
    db.session.commit()

    return jsonify({}), 204 