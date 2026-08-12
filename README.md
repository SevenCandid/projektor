# Projektor

**Discover. Build. Showcase.**

Projektor is a digital platform where students and learners from different institutions can showcase, discover, and explore academic, personal, technical, creative, and research projects.

This project was built primarily as a **Database Course Project** to demonstrate the design, implementation, and use of a relational MySQL database.

## Architecture

* **Database (Core):** MySQL. All schemas and seed data are managed directly via SQL scripts.
* **Backend:** Python + Flask. Serves as a REST API layer that queries the database.
* **Frontend:** HTML5 + CSS3 + Vanilla JavaScript. A responsive, dynamic presentation layer connecting to the API via Fetch.

## Setup Instructions

### 1. Database Initialization
Ensure you have XAMPP installed and running (Apache + MySQL).
Run the following SQL scripts in order (via phpMyAdmin or MySQL CLI) to create and populate the database:
1. `database/01_create_database.sql`
2. `database/02_create_tables.sql`
3. `database/03_insert_seed_data.sql`

### 2. Backend Setup
Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
```
*(Note: Ensure you have `Flask`, `mysql-connector-python`, `python-dotenv`, `Flask-CORS`, `Flask-Bcrypt`, and `werkzeug` installed if `requirements.txt` is missing).*

Create a `.env` file in the root directory:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=projektor_db

FLASK_SECRET_KEY=super_secret_key_for_projektor_mvp
```

Run the API server:
```bash
cd backend
python app.py
```

### 3. Frontend Setup
Open the `frontend` folder and serve the HTML files. You can use VS Code's "Live Server" extension, or Python's built-in HTTP server:
```bash
cd frontend
python -m http.server 8000
```
Then visit `http://localhost:8000` in your web browser.

## Features
- **Project Discovery:** Search and filter student projects.
- **Authentication:** Secure user registration and login (bcrypt + sessions).
- **Project Management:** Create, edit, and delete your own projects.
- **Dynamic Metadata:** Taxonomies managed relationally in MySQL.
- **Modern UI:** Responsive, glassmorphism design with a dark mode aesthetic.
