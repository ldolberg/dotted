from .session import engine, Base
from .models import User


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine) 