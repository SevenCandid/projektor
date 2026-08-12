import os
import json
import time
from flask import Blueprint, jsonify, request, session, current_app
from database import get_db_connection
from utils.auth import login_required
from werkzeug.utils import secure_filename

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('', methods=['GET'])
def get_all_projects():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    search_query = request.args.get('search', '')
    category_id = request.args.get('category', '')
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        user_id = session.get('user_id', 0)
        query = """
            SELECT p.id, p.title, p.description, p.image_url, p.status, c.name as category, u.full_name as author, u.profile_image as author_image,
                   (SELECT COUNT(*) FROM likes WHERE project_id = p.id) as like_count,
                   (SELECT COUNT(*) FROM comments WHERE project_id = p.id) as comment_count,
                   EXISTS(SELECT 1 FROM likes WHERE project_id = p.id AND user_id = %s) as has_liked
            FROM projects p
            JOIN categories c ON p.category_id = c.id
            JOIN users u ON p.user_id = u.id
            WHERE 1=1
        """
        params = [user_id]
        
        if search_query:
            query += " AND (p.title LIKE %s OR p.description LIKE %s)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])
            
        if category_id:
            query += " AND p.category_id = %s"
            params.append(category_id)
            
        query += " ORDER BY p.created_at DESC"
        
        cursor.execute(query, params)
        projects = cursor.fetchall()
        return jsonify(projects), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        user_id = session.get('user_id', 0)
        # Get project details
        cursor.execute("""
            SELECT p.*, c.name as category, u.full_name as author, u.institution, u.profile_image as author_image,
                   (SELECT COUNT(*) FROM likes WHERE project_id = p.id) as like_count,
                   (SELECT COUNT(*) FROM comments WHERE project_id = p.id) as comment_count,
                   EXISTS(SELECT 1 FROM likes WHERE project_id = p.id AND user_id = %s) as has_liked
            FROM projects p
            JOIN categories c ON p.category_id = c.id
            JOIN users u ON p.user_id = u.id
            WHERE p.id = %s
        """, (user_id, project_id))
        project = cursor.fetchone()
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
            
        # Get technologies
        cursor.execute("""
            SELECT t.id, t.name
            FROM technologies t
            JOIN project_technologies pt ON t.id = pt.technology_id
            WHERE pt.project_id = %s
        """, (project_id,))
        project['technologies'] = cursor.fetchall()
        
        return jsonify(project), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


def parse_request_data():
    """Helper to parse JSON or FormData safely."""
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        data = request.form.to_dict()
        if 'technologies' in data and data['technologies']:
            try:
                data['technologies'] = json.loads(data['technologies'])
            except:
                data['technologies'] = []
        else:
            data['technologies'] = []
            
        if 'new_technologies' in data and data['new_technologies']:
            try:
                data['new_technologies'] = json.loads(data['new_technologies'])
            except:
                data['new_technologies'] = []
        else:
            data['new_technologies'] = []
            
        # Also parse existing_images if passed
        if 'existing_images' in data and data['existing_images']:
            try:
                data['existing_images'] = json.loads(data['existing_images'])
            except:
                data['existing_images'] = []
                
        return data
    else:
        return request.json or {}

@projects_bp.route('', methods=['POST'])
@login_required
def create_project():
    data = parse_request_data()
    user_id = session['user_id']
    
    title = data.get('title')
    description = data.get('description')
    category_id = data.get('category_id')
    technologies = data.get('technologies', [])
    new_technologies = data.get('new_technologies', [])
    
    if not title or not description or not category_id:
        return jsonify({"error": "Missing required fields"}), 400
        
    # Handle image uploads
    image_urls = []
    if request.content_type and request.content_type.startswith('multipart/form-data'):
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file and file.filename:
                    try:
                        import cloudinary.uploader
                        upload_result = cloudinary.uploader.upload(file)
                        image_urls.append(upload_result.get('secure_url'))
                    except Exception as e:
                        return jsonify({"error": f"Image upload failed: {str(e)}"}), 500
    else:
        # Fallback if old JSON is used
        if data.get('image_url'):
            image_urls = [data.get('image_url')]

    final_image_url = ",".join(image_urls) if image_urls else None

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO projects (user_id, category_id, title, description, image_url, github_url, demo_url, status, academic_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_id, category_id, title, description,
            final_image_url, data.get('github_url'), data.get('demo_url'),
            data.get('status', 'In Progress'), data.get('academic_year')
        ))
        
        project_id = cursor.lastrowid
        
        if new_technologies:
            for tech in new_technologies:
                cursor.execute("SELECT id FROM technologies WHERE LOWER(name) = LOWER(%s)", (tech,))
                row = cursor.fetchone()
                if row:
                    technologies.append(row[0])
                else:
                    cursor.execute("INSERT INTO technologies (name) VALUES (%s)", (tech,))
                    technologies.append(cursor.lastrowid)

        if technologies:
            tech_query = "INSERT INTO project_technologies (project_id, technology_id) VALUES (%s, %s)"
            tech_data = [(project_id, tech_id) for tech_id in technologies]
            cursor.executemany(tech_query, tech_data)
            
        conn.commit()
        return jsonify({"message": "Project created successfully", "project_id": project_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@projects_bp.route('/<int:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    data = parse_request_data()
    user_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, image_url FROM projects WHERE id = %s", (project_id,))
        project = cursor.fetchone()
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        if project['user_id'] != user_id:
            return jsonify({"error": "Unauthorized to update this project"}), 403
            
        # Handle images
        existing_images = data.get('existing_images', [])
        image_urls = existing_images.copy() if isinstance(existing_images, list) else []
        
        # Add new uploaded images
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            if 'images' in request.files:
                files = request.files.getlist('images')
                for file in files:
                    if file and file.filename:
                        try:
                            import cloudinary.uploader
                            upload_result = cloudinary.uploader.upload(file)
                            image_urls.append(upload_result.get('secure_url'))
                        except Exception as e:
                            return jsonify({"error": f"Image upload failed: {str(e)}"}), 500
                        
        final_image_url = ",".join(image_urls) if image_urls else None

        # Optionally delete old files that are no longer in image_urls
        old_urls = project['image_url'].split(',') if project['image_url'] else []
        for old_url in old_urls:
            if old_url and old_url not in image_urls:
                # Remove file from cloudinary (Extract public_id if needed, ignoring for now)
                pass
            
        # Update project
        query = """
            UPDATE projects 
            SET category_id = %s, title = %s, description = %s, image_url = %s, 
                github_url = %s, demo_url = %s, status = %s, academic_year = %s
            WHERE id = %s
        """
        cursor.execute(query, (
            data.get('category_id'), data.get('title'), data.get('description'),
            final_image_url, data.get('github_url'), data.get('demo_url'),
            data.get('status'), data.get('academic_year'), project_id
        ))
        
        technologies = data.get('technologies')
        new_technologies = data.get('new_technologies', [])
        if new_technologies:
            if technologies is None:
                technologies = []
            for tech in new_technologies:
                cursor.execute("SELECT id FROM technologies WHERE LOWER(name) = LOWER(%s)", (tech,))
                row = cursor.fetchone()
                if row:
                    technologies.append(row['id'])
                else:
                    cursor.execute("INSERT INTO technologies (name) VALUES (%s)", (tech,))
                    technologies.append(cursor.lastrowid)

        if technologies is not None:
            cursor.execute("DELETE FROM project_technologies WHERE project_id = %s", (project_id,))
            if technologies:
                tech_query = "INSERT INTO project_technologies (project_id, technology_id) VALUES (%s, %s)"
                tech_data = [(project_id, tech_id) for tech_id in technologies]
                cursor.executemany(tech_query, tech_data)
                
        conn.commit()
        return jsonify({"message": "Project updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    user_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, image_url FROM projects WHERE id = %s", (project_id,))
        project = cursor.fetchone()
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        if project['user_id'] != user_id:
            return jsonify({"error": "Unauthorized to delete this project"}), 403
            
        # Delete files
        old_urls = project['image_url'].split(',') if project['image_url'] else []
        for old_url in old_urls:
            if old_url:
                # Remove file from cloudinary (Extract public_id if needed, ignoring for now)
                pass
                    
        cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        conn.commit()
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@projects_bp.route('/<int:project_id>/like', methods=['POST'])
@login_required
def toggle_like(project_id):
    user_id = session['user_id']
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        # Check if already liked
        cursor.execute("SELECT id FROM likes WHERE user_id = %s AND project_id = %s", (user_id, project_id))
        existing_like = cursor.fetchone()
        
        if existing_like:
            cursor.execute("DELETE FROM likes WHERE id = %s", (existing_like['id'],))
            liked = False
        else:
            cursor.execute("INSERT INTO likes (user_id, project_id) VALUES (%s, %s)", (user_id, project_id))
            liked = True
            
        conn.commit()
        
        # Get updated count
        cursor.execute("SELECT COUNT(*) as count FROM likes WHERE project_id = %s", (project_id,))
        count = cursor.fetchone()['count']
        
        return jsonify({"message": "Success", "has_liked": liked, "like_count": count}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@projects_bp.route('/<int:project_id>/comments', methods=['GET'])
def get_comments(project_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.id, c.content, c.created_at, u.id as user_id, u.full_name, u.profile_image
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.project_id = %s
            ORDER BY c.created_at ASC
        """
        cursor.execute(query, (project_id,))
        comments = cursor.fetchall()
        return jsonify(comments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@projects_bp.route('/<int:project_id>/comments', methods=['POST'])
@login_required
def add_comment(project_id):
    user_id = session['user_id']
    data = request.json or {}
    content = data.get('content')
    
    if not content or not content.strip():
        return jsonify({"error": "Comment content cannot be empty"}), 400
        
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Insert comment
        cursor.execute(
            "INSERT INTO comments (user_id, project_id, content) VALUES (%s, %s, %s)",
            (user_id, project_id, content.strip())
        )
        conn.commit()
        
        comment_id = cursor.lastrowid
        
        # Fetch the newly created comment to return it
        cursor.execute("""
            SELECT c.id, c.content, c.created_at, u.id as user_id, u.full_name
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
        """, (comment_id,))
        new_comment = cursor.fetchone()
        
        return jsonify(new_comment), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@projects_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    user_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verify ownership
        cursor.execute("SELECT user_id FROM comments WHERE id = %s", (comment_id,))
        comment = cursor.fetchone()
        
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
            
        if comment['user_id'] != user_id:
            return jsonify({"error": "Unauthorized"}), 403
            
        cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
        conn.commit()
        
        return jsonify({"message": "Comment deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
