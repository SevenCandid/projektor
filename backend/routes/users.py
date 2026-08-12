from flask import Blueprint, jsonify, request, session
from database import get_db_connection
from utils.auth import login_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        # Get user details
        cursor.execute("""
            SELECT id, full_name, institution, program, level, bio, profile_image, created_at 
            FROM users 
            WHERE id = %s
        """, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Get user's projects
        cursor.execute("""
            SELECT p.id, p.title, p.description, p.status, p.academic_year, c.name as category
            FROM projects p
            JOIN categories c ON p.category_id = c.id
            WHERE p.user_id = %s
        """, (user_id,))
        user['projects'] = cursor.fetchall()
        
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@users_bp.route('/me', methods=['PUT'])
@login_required
def update_profile():
    user_id = session['user_id']
    data = request.json
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor()
        query = """
            UPDATE users 
            SET full_name = %s, institution = %s, program = %s, level = %s, bio = %s
            WHERE id = %s
        """
        cursor.execute(query, (
            data.get('full_name'), 
            data.get('institution'), 
            data.get('program'), 
            data.get('level'), 
            data.get('bio'), 
            user_id
        ))
        conn.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

import os
import time
from werkzeug.utils import secure_filename
from flask import current_app

@users_bp.route('/me/image', methods=['POST'])
@login_required
def upload_profile_image():
    user_id = session['user_id']
    
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        try:
            import cloudinary.uploader
            upload_result = cloudinary.uploader.upload(file)
            image_url = upload_result.get('secure_url')
        except Exception as e:
            return jsonify({"error": f"Cloudinary upload failed: {str(e)}"}), 500
        
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
            
        try:
            cursor = conn.cursor()
            
            cursor.execute("UPDATE users SET profile_image = %s WHERE id = %s", (image_url, user_id))
            conn.commit()
            
            return jsonify({"message": "Profile image updated", "profile_image": image_url}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    
    return jsonify({"error": "File processing failed"}), 500
