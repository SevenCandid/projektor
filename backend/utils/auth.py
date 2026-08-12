from functools import wraps
from flask import session, jsonify

def login_required(f):
    """
    Decorator to ensure that a user is logged in before accessing a route.
    If the user is not logged in, returns a 401 Unauthorized response.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized. Please log in."}), 401
        return f(*args, **kwargs)
    return decorated_function
