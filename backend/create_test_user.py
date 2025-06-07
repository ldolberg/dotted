#!/usr/bin/env python3
"""Create a test admin user for development."""

from app.db.session import get_db
from app.crud.user import create_user
import json

def create_test_user():
    """Create a test admin user."""
    db = next(get_db())
    try:
        user = create_user(
            db=db,
            email='admin@test.com',
            name='Test Admin',
            password='admin123',
            roles=json.dumps(['ADMIN'])
        )
        print(f'Created test user: {user.email} with roles: {user.roles}')
        return user
    except Exception as e:
        print(f'Error creating user (might already exist): {e}')
        return None
    finally:
        db.close()

if __name__ == '__main__':
    create_test_user() 