from flask import Blueprint, request, jsonify, session
from flask_bcrypt import Bcrypt
from database import get_db_connection

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')
    institution = data.get('institution', None)
    program = data.get('program', None)
    level = data.get('level', None)
    
    if not full_name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO users (full_name, email, password_hash, institution, program, level)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (full_name, email, hashed_password, institution, program, level))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        # e.g., email already exists
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, full_name, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": user['id'],
                    "full_name": user['full_name'],
                    "email": email
                }
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('full_name', None)
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route('/me', methods=['GET'])
def get_me():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT profile_image FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                profile_image = user['profile_image'] if user else None
                return jsonify({
                    "user_id": user_id, 
                    "full_name": session.get('full_name'),
                    "profile_image": profile_image
                }), 200
            except Exception:
                pass
            finally:
                cursor.close()
                conn.close()
        return jsonify({"user_id": user_id, "full_name": session.get('full_name')}), 200
    return jsonify({"error": "Not logged in"}), 401
