# SQLAlchemy models
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from .session import Base
# Remove this: from passlib.hash import pbkdf2_sha256 # Import the hashing library
# Remove this: from app.crud.user import pwd_context # We are now importing verify_password from security
from app.core.security import verify_password # Import verify_password

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hashed password using the application's password context."""
        # Change this line to use verify_password from security.py
        return verify_password(password, self.hashed_password)