# SQLAlchemy models
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from .session import Base
# Remove this: from passlib.hash import pbkdf2_sha256 # Import the hashing library
# Remove this: from app.crud.user import pwd_context # We are now importing verify_password from security
from app.core.security import verify_password # Import verify_password
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship # Import relationship
from sqlalchemy import ForeignKey, Enum # Import ForeignKey and Enum
# from flask_sqlalchemy import SQLAlchemy # No longer needed
# db = SQLAlchemy() # No longer needed

# Import db from extensions.py
from app.extensions import db

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    roles = Column(String, default=list)

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hashed password using the application's password context."""
        # Change this line to use verify_password from security.py
        return verify_password(password, self.hashed_password)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    address_street = db.Column(db.String(255), nullable=True)
    address_city = db.Column(db.String(100), nullable=True)
    address_state = db.Column(db.String(100), nullable=True)
    address_zip = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    # Relationship
    communication_preference = relationship('CommunicationPreference', back_populates='patient', uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": str(self.id), "first_name": self.first_name, "last_name": self.last_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "email": self.email, "phone_number": self.phone_number,
            "address_street": self.address_street, "address_city": self.address_city,
            "address_state": self.address_state, "address_zip": self.address_zip,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "communication_preference": self.communication_preference.to_dict() if self.communication_preference else None
        }

class CommunicationPreference(db.Model):
    __tablename__ = 'communication_preferences'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('patients.id'), nullable=False, unique=True)
    preferred_method = db.Column(Enum('EMAIL', 'SMS', 'PHONE', name='comm_method_enum'), default='EMAIL', nullable=False)
    allows_appointment_reminders = db.Column(db.Boolean, default=True, nullable=False)
    allows_billing_notifications = db.Column(db.Boolean, default=True, nullable=False)
    allows_marketing_updates = db.Column(db.Boolean, default=False, nullable=False)
    # Relationship
    patient = relationship('Patient', back_populates='communication_preference')

    def to_dict(self):
        return {
            "id": str(self.id),
            "patient_id": str(self.patient_id),
            "preferred_method": self.preferred_method,
            "allows_appointment_reminders": self.allows_appointment_reminders,
            "allows_billing_notifications": self.allows_billing_notifications,
            "allows_marketing_updates": self.allows_marketing_updates,
        }