# User CRUD operations
from sqlalchemy.orm import Session
# Remove this import: from passlib.context import CryptContext
from app.db.models import User
from app.core.security import get_password_hash # Import get_password_hash

# Remove this entire block (including the pwd_context definition and the two functions):
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def get_password_hash(password: str) -> str:
#     """Hash a password."""
#     return pwd_context.hash(password)
#
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a password against its hash."""
#     return pwd_context.verify(plain_password, hashed_password)


def get_user_by_email(db: Session, email: str):
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str, name: str, password: str):
    """Create a new user."""
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        name=name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user