from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt # Import necessary functions
from werkzeug.exceptions import NotFound # Import NotFound

def token_required(allowed_roles=None):
    """
    Decorator to protect endpoints. Requires a valid JWT token.
    Optionally checks if the user has one of the allowed roles.
    """
    if allowed_roles is None:
        allowed_roles = []

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                print("DEBUG: Entering token_required decorator")
                verify_jwt_in_request()
                print("DEBUG: verify_jwt_in_request passed")
                current_user_identity = get_jwt_identity()
                claims = get_jwt() # Get the claims from the token
                print(f"DEBUG: User identity: {current_user_identity}, Claims: {claims}")

                # Assuming roles are stored in the 'roles' claim
                user_roles = claims.get('roles', [])
                print(f"DEBUG: User roles: {user_roles}, Allowed roles: {allowed_roles}")

                if allowed_roles:
                    # Check if the user has at least one of the allowed roles
                    if not any(role in allowed_roles for role in user_roles):
                         print("DEBUG: Role check failed, returning 403")
                         return jsonify({'msg': 'User does not have required roles'}), 403

                print("DEBUG: Role check passed, executing route function")
                # You might want to pass the user identity or other info to the route handler
                # For now, we just ensure the token is valid and roles are checked.
                response = fn(*args, **kwargs)
                return response
            except Exception as e:
                # Handle specific JWT errors if needed, e.g., InvalidTokenError
                print(f"DEBUG: Exception in token_required: {e}")
                # If the exception is NotFound, re-raise it to allow Flask's 404 handler to take over
                if isinstance(e, NotFound):
                    print("DEBUG: Caught NotFound exception, re-raising it")
                    raise e # Re-raise the NotFound exception
                print("DEBUG: Returning 401 for authentication or other unexpected error")
                return jsonify({'msg': str(e)}), 401 # Return 401 for authentication errors

        return decorator
    return wrapper 