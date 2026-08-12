import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Import Blueprints
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.users import users_bp
from routes.metadata import metadata_bp

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path, override=True)
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    secure=True
    # CLOUDINARY_URL from env will automatically be used
)

app = Flask(__name__)
# Enable CORS for the frontend origin
CORS(app, supports_credentials=True)

# Secret key is required for session management
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key_if_not_set")

# Required for cross-origin cookies (Vercel Frontend -> Render Backend)
app.config.update(
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True
)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(projects_bp, url_prefix='/api/projects')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(metadata_bp, url_prefix='/api')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Projektor API is running!"}), 200

# Serve uploaded images statically
@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    uploads_dir = os.path.join(app.root_path, 'uploads')
    return send_from_directory(uploads_dir, filename)

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

# 500 error handler temporarily removed for debugging

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
