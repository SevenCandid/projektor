from flask import Blueprint, jsonify, request, session
from database import get_db_connection
from utils.auth import login_required

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
        
        query = """
            SELECT p.id, p.title, p.description, p.image_url, p.status, c.name as category, u.full_name as author
            FROM projects p
            JOIN categories c ON p.category_id = c.id
            JOIN users u ON p.user_id = u.id
            WHERE 1=1
        """
        params = []
        
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
        # Get project details
        cursor.execute("""
            SELECT p.*, c.name as category, u.full_name as author, u.institution
            FROM projects p
            JOIN categories c ON p.category_id = c.id
            JOIN users u ON p.user_id = u.id
            WHERE p.id = %s
        """, (project_id,))
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


@projects_bp.route('', methods=['POST'])
@login_required
def create_project():
    data = request.json
    user_id = session['user_id']
    
    title = data.get('title')
    description = data.get('description')
    category_id = data.get('category_id')
    technologies = data.get('technologies', [])
    new_technologies = data.get('new_technologies', [])
    
    if not title or not description or not category_id:
        return jsonify({"error": "Missing required fields"}), 400
        
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor()
        # Insert project
        query = """
            INSERT INTO projects (user_id, category_id, title, description, image_url, github_url, demo_url, status, academic_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            user_id, category_id, title, description,
            data.get('image_url'), data.get('github_url'), data.get('demo_url'),
            data.get('status', 'In Progress'), data.get('academic_year')
        ))
        
        project_id = cursor.lastrowid
        
        # Process new technologies
        if new_technologies:
            for tech in new_technologies:
                # Check if exists (case insensitive)
                cursor.execute("SELECT id FROM technologies WHERE LOWER(name) = LOWER(%s)", (tech,))
                row = cursor.fetchone()
                if row:
                    technologies.append(row[0])
                else:
                    cursor.execute("INSERT INTO technologies (name) VALUES (%s)", (tech,))
                    technologies.append(cursor.lastrowid)

        # Insert technologies
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
    data = request.json
    user_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        # Check ownership
        cursor.execute("SELECT user_id FROM projects WHERE id = %s", (project_id,))
        project = cursor.fetchone()
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        if project['user_id'] != user_id:
            return jsonify({"error": "Unauthorized to update this project"}), 403
            
        # Update project
        query = """
            UPDATE projects 
            SET category_id = %s, title = %s, description = %s, image_url = %s, 
                github_url = %s, demo_url = %s, status = %s, academic_year = %s
            WHERE id = %s
        """
        cursor.execute(query, (
            data.get('category_id'), data.get('title'), data.get('description'),
            data.get('image_url'), data.get('github_url'), data.get('demo_url'),
            data.get('status'), data.get('academic_year'), project_id
        ))
        
        technologies = data.get('technologies')
        # Process new technologies
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

        # Update technologies (delete existing, then insert new)
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
        # Check ownership
        cursor.execute("SELECT user_id FROM projects WHERE id = %s", (project_id,))
        project = cursor.fetchone()
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        if project['user_id'] != user_id:
            return jsonify({"error": "Unauthorized to delete this project"}), 403
            
        # Delete project (ON DELETE CASCADE will handle project_technologies)
        cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        conn.commit()
        return jsonify({"message": "Project deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
