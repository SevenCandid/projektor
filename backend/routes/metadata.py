from flask import Blueprint, jsonify
from database import get_db_connection

metadata_bp = Blueprint('metadata', __name__)

@metadata_bp.route('/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, description FROM categories ORDER BY name ASC")
        categories = cursor.fetchall()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@metadata_bp.route('/technologies', methods=['GET'])
def get_technologies():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM technologies ORDER BY name ASC")
        technologies = cursor.fetchall()
        return jsonify(technologies), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
