# PROJEKTOR — Master Implementation Specification

## 1. Project Identity

**Product Name:** Projektor

**Tagline:** Discover. Build. Showcase.

**Description:**

Projektor is a digital platform where students and learners from different institutions can showcase, discover, and explore academic, personal, technical, creative, and research projects.

The platform should feel like a polished real-world product, not a school assignment.

The initial MVP is being developed as a database-driven web application.

---

# 2. Technology Stack & Architecture

> **MySQL is the core/data layer of Projektor.**
>
> **SQL defines and operates on the database.**
>
> **Python/Flask is the application/backend layer that communicates with the database.**
>
> **JavaScript/HTML/CSS is the presentation layer that presents the database functionality to the user.**

**Architecture Flow:**
FRONTEND (HTML + CSS + JavaScript)
↓ (HTTP / API)
BACKEND (Python + Flask)
↓ (SQL queries)
DATABASE (MySQL -> projektor_db)
↓
users, projects, categories, technologies, project_technologies

Use exactly the following stack unless there is a strong technical reason otherwise:

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Responsive design
* Fetch API for communicating with the backend

### Backend

* Python
* Flask
* REST-style API
* Flask-CORS if required

### Database

* MySQL

### Development

* Gemini/Antigravity IDE
* MySQL local development environment
* Python virtual environment

Do NOT introduce React, Vue, Angular, Django, Node.js, Firebase, Supabase, PostgreSQL, or another major framework/database.

The goal is to keep the architecture simple and easy to understand for a database course presentation.

---

# 3. Core MVP Goal

The MVP must allow a user to:

1. Register
2. Log in
3. Maintain basic profile information
4. Create a project
5. View their projects
6. Edit their projects
7. Delete their projects
8. Browse projects from other users
9. Search projects
10. Filter projects by category/status
11. Open a project's details
12. See the project's creator and related information

The application must demonstrate real CRUD operations against MySQL.

---

# 4. User Concept

There is one primary user type:

## Student / Learner

A registered user can publish projects.

The platform should NOT be restricted to a particular university.

Users may optionally provide:

* Institution
* Program
* Level / Year
* Bio
* Profile image

These fields should not prevent someone from registering if they are unknown or not applicable.

Example:

Frank Bediako
University of Energy and Natural Resources
BSc Computer Engineering
Level 300

Another user could simply be:

Ama Mensah
University of Ghana
BSc Computer Science
Level 200

Another user could have no institution information.

---

# 5. Database Design

Create the following five tables.

## 5.1 users

Fields:

* id — INT, PRIMARY KEY, AUTO_INCREMENT
* full_name — VARCHAR(100), NOT NULL
* email — VARCHAR(150), NOT NULL, UNIQUE
* password_hash — VARCHAR(255), NOT NULL
* institution — VARCHAR(150), NULL
* program — VARCHAR(150), NULL
* level — VARCHAR(30), NULL
* bio — TEXT, NULL
* profile_image — VARCHAR(500), NULL
* created_at — TIMESTAMP, DEFAULT CURRENT_TIMESTAMP

Passwords MUST NOT be stored as plain text.

Use secure password hashing such as Werkzeug's password hashing utilities.

---

## 5.2 categories

Fields:

* id — INT, PRIMARY KEY, AUTO_INCREMENT
* name — VARCHAR(100), NOT NULL, UNIQUE
* description — VARCHAR(255), NULL

Seed the database with:

* Web Development
* Mobile Development
* Artificial Intelligence
* Machine Learning
* Data Science
* IoT & Embedded Systems
* Robotics
* Electronics
* Cybersecurity
* Networking
* Research
* Design & Creative
* Business & Entrepreneurship
* Other

---

## 5.3 projects

Fields:

* id — INT, PRIMARY KEY, AUTO_INCREMENT
* user_id — INT, NOT NULL
* category_id — INT, NOT NULL
* title — VARCHAR(200), NOT NULL
* description — TEXT, NOT NULL
* image_url — VARCHAR(500), NULL
* github_url — VARCHAR(500), NULL
* demo_url — VARCHAR(500), NULL
* status — ENUM('In Progress', 'Completed', 'Archived'), DEFAULT 'In Progress'
* academic_year — VARCHAR(20), NULL
* created_at — TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
* updated_at — TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

Foreign keys:

user_id → users.id

category_id → categories.id

Use appropriate ON DELETE behavior.

A project belongs to one user.

A user can have many projects.

A project belongs to one category.

A category can contain many projects.

---

## 5.4 technologies

Fields:

* id — INT, PRIMARY KEY, AUTO_INCREMENT
* name — VARCHAR(100), NOT NULL, UNIQUE

Seed with common technologies such as:

* HTML
* CSS
* JavaScript
* Python
* Flask
* MySQL
* C++
* Java
* PHP
* Node.js
* React
* Arduino
* ESP32
* Git
* GitHub

---

## 5.5 project_technologies

This is the junction table for the many-to-many relationship between projects and technologies.

Fields:

* project_id — INT, NOT NULL
* technology_id — INT, NOT NULL

Use a composite primary key:

PRIMARY KEY (project_id, technology_id)

Foreign keys:

project_id → projects.id

technology_id → technologies.id

A project can use many technologies.

A technology can belong to many projects.

---

# 6. Database Relationship Summary

Implement these relationships:

### users → projects

One-to-many.

One user can create many projects.

### categories → projects

One-to-many.

One category can contain many projects.

### projects ↔ technologies

Many-to-many through project_technologies.

The database design should be normalized appropriately for the MVP.

Do not unnecessarily create additional tables for institutions, programs, levels, etc.

---

# 7. Application Pages

Create the following pages/views.

## 7.1 Home

Route:

/

Purpose:

Introduce Projektor and show recent/featured projects.

Sections:

### Navigation

Logo:

PROJEKTOR

Navigation:

* Home
* Explore
* Login / Dashboard depending on authentication state

Primary CTA:

Showcase Your Project

### Hero

Display:

"Discover. Build. Showcase."

Supporting text:

"A place for students to share the projects they're building and discover what others are creating."

Buttons:

Explore Projects

Showcase Your Project

### Recent Projects

Display several project cards retrieved from MySQL.

### Categories

Display project categories.

### Footer

Keep it simple.

---

# 8. Explore Projects

Route:

/projects

Purpose:

Allow visitors to discover projects.

Features:

* Search
* Category filter
* Status filter
* Project cards
* Pagination or simple limited result set if necessary

Search should query the backend/database.

Example:

/api/projects?search=python

Category example:

/api/projects?category=Web Development

Status example:

/api/projects?status=Completed

Multiple filters should work together where practical.

Project cards should show:

* Project image
* Project title
* Category
* Status
* Creator name
* Institution if available
* Technologies
* View Project button

---

# 9. Project Details

Route:

/projects/:id

Display:

* Project image
* Project title
* Description
* Category
* Status
* Academic year if available
* Creator name
* Creator institution
* Creator program
* Creator level
* Technologies
* GitHub link if available
* Live demo link if available

This page should demonstrate retrieval of related data from multiple tables.

For example:

projects
JOIN users
JOIN categories
JOIN project_technologies
JOIN technologies

---

# 10. Registration

Route:

/register

Fields:

Required:

* Full name
* Email
* Password

Optional:

* Institution
* Program
* Level / Year

Validate input.

Prevent duplicate email addresses.

Hash passwords securely.

After successful registration, redirect to login or automatically authenticate the user.

---

# 11. Login

Route:

/login

Fields:

* Email
* Password

Authenticate against MySQL.

Do not store passwords in plain text.

Use a simple secure authentication mechanism appropriate for Flask.

The implementation can use session-based authentication or another simple secure approach, but keep the architecture understandable.

---

# 12. Dashboard

Route:

/dashboard

Only authenticated users should access this page.

Display:

* User name
* Institution
* Program
* Number of projects
* Project list

Actions:

* Create project
* View project
* Edit project
* Delete project
* Edit profile
* Logout

Example:

"Welcome back, Frank"

"My Projects"

"3 Projects"

---

# 13. Create Project

Route:

/projects/new

Fields:

### Required

* Project title
* Description
* Category
* Status

### Optional

* Technologies
* Academic year
* Project image URL
* GitHub URL
* Live demo URL

For the MVP, use an image URL instead of implementing file uploads.

The user should be able to select multiple technologies.

After submission:

1. Validate data.
2. Insert project into projects table.
3. Insert project/technology relationships into project_technologies.
4. Redirect to dashboard or project details.

---

# 14. Edit Project

Route:

/projects/:id/edit

Only the owner of the project should be allowed to edit it.

Populate the form with existing information.

On submission:

1. Validate data.
2. Update projects.
3. Remove old project_technologies relationships.
4. Insert the updated technology relationships.
5. Redirect to project details/dashboard.

---

# 15. Delete Project

Only the project owner can delete a project.

Show a confirmation dialog before deletion.

When confirmed:

1. Delete related project_technologies records.
2. Delete the project.
3. Return to dashboard.

Do not allow a user to delete another user's project.

---

# 16. Profile

Allow authenticated users to view and update their profile.

Fields:

* Full name
* Institution
* Program
* Level
* Bio
* Profile image URL

Email can remain read-only in the MVP.

---

# 17. REST API

Implement the following API endpoints.

## Authentication

POST /api/auth/register

POST /api/auth/login

POST /api/auth/logout

GET /api/auth/me

## Projects

GET /api/projects

GET /api/projects/:id

POST /api/projects

PUT /api/projects/:id

DELETE /api/projects/:id

## Categories

GET /api/categories

## Technologies

GET /api/technologies

## User

GET /api/users/:id

PUT /api/users/me

---

# 18. Project API Behavior

GET /api/projects should support:

* Search
* Category filtering
* Status filtering

Example:

GET /api/projects?search=python

GET /api/projects?category=Web Development

GET /api/projects?status=Completed

GET /api/projects?search=python&status=Completed

Return clean JSON responses.

Include useful project information such as:

* id
* title
* description
* category
* status
* image
* creator
* technologies
* created_at

Do not expose password_hash.

---

# 19. Security

Implement basic security appropriate for an academic MVP.

Requirements:

* Password hashing
* Input validation
* Parameterized SQL queries
* Do not expose database credentials to frontend
* Do not return password hashes in API responses
* Authentication checks for protected routes
* Authorization checks for project editing/deletion
* Validate URLs where practical
* Handle database errors gracefully

Use environment variables for:

* MySQL host
* MySQL user
* MySQL password
* MySQL database
* Flask secret key

Provide a `.env.example`.

Do not hard-code real credentials.

---

# 20. Frontend Design

The interface should be modern, clean, minimal, and responsive.

Avoid an overly complicated dashboard.

Visual direction:

* Professional technology/startup aesthetic
* Plenty of whitespace
* Clear typography
* Modern cards
* Rounded corners used moderately
* Subtle shadows
* Strong visual hierarchy
* Responsive navigation
* Mobile-friendly project cards
* Clean forms
* Clear buttons
* Good empty states
* Good loading states
* Good error messages

Do not overcrowd the interface.

Projektor should look like a real product.

---

# 21. Brand

Use:

PROJEKTOR

Tagline:

Discover. Build. Showcase.

Do not use "UENR" or another specific institution as the main branding.

The platform must remain institution-independent.

---

# 22. Sample Data

Seed enough realistic data to make the application look populated immediately.

Create at least:

5–8 users

10–15 projects

All major categories

10–15 technologies

Create realistic relationships between projects and technologies.

Example projects:

### Smart Home Automation System

Category:
IoT & Embedded Systems

Technologies:
ESP32, Arduino, C++

Status:
Completed

### Student Expense Tracker

Category:
Web Development

Technologies:
HTML, CSS, JavaScript, Python, MySQL

Status:
In Progress

### Campus Navigation System

Category:
Software

Technologies:
JavaScript, Python, MySQL

Status:
Completed

Also include projects from different institutions.

---

# 23. Recommended Folder Structure

Use a clean structure similar to:

projektor/

├── backend/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── auth.py
│   │   ├── projects.py
│   │   ├── users.py
│   │   └── metadata.py
│   └── utils/
│       └── auth.py
│
├── frontend/
│   ├── index.html
│   ├── projects.html
│   ├── project-details.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── project-form.html
│   ├── profile.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── api.js
│       ├── auth.js
│       ├── projects.js
│       ├── dashboard.js
│       └── main.js
│
├── database/
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_insert_seed_data.sql
│   ├── 04_sample_queries.sql
│   └── 05_test_queries.sql
│
├── .env.example
├── .gitignore
└── README.md

The exact structure may be adjusted if needed, but keep frontend, backend, and database responsibilities clearly separated.

Python should NOT define the database schema, create the database, create tables, or seed data. All database structures and initial data must be defined in the `.sql` files.

---

# 24. Development Order

Build the project in this order. Do NOT proceed to later phases until the current phase is verified.

## PHASE 1
MySQL database creation + schema + seed data
* Create project
* Create Python virtual environment
* Configure `.env`
* Create `01_create_database.sql`, `02_create_tables.sql`, `03_insert_seed_data.sql`
* Execute SQL to create and populate the database

## PHASE 2
Test and demonstrate SQL queries
* Create `04_sample_queries.sql` and `05_test_queries.sql`
* Run queries directly against MySQL to prove relationships and operations work

## PHASE 3
Flask/MySQL connection
* Install Flask and dependencies
* Configure `database.py` to establish connection using `.env`
* Verify Python can connect to MySQL

## PHASE 4
Backend CRUD API
* Implement Authentication
* Implement Project CRUD
* Implement Categories & Technologies
* Implement User/profile endpoints
* Implement Search/filtering
* Test APIs locally

## PHASE 5
Frontend integration
* Build HTML templates and CSS
* Connect frontend to Flask API using Fetch API
* Verify Register, Login, Create, Edit, Delete, Explore, and Details pages

## PHASE 6
Authentication and authorization
* Secure endpoints
* Session/JWT validation
* Access controls (users only edit their own projects)

## PHASE 7
UI polish and final testing
* Responsive design
* Loading and empty states
* Error handling
* Final end-to-end tests

---

# 25. Important MVP Boundaries

DO NOT build these features in the MVP:

* Comments
* Likes
* Following
* Messaging
* Notifications
* Social feed
* Admin dashboard
* Email verification
* Password reset
* Google authentication
* File storage service
* Real-time communication
* AI recommendations
* Recommendation engine
* Chatbot
* Complex analytics
* Payment system
* Institution administration
* Team collaboration
* Project competitions

These can be future features.

Do not expand the scope unless explicitly instructed.

---

# 26. Database Demonstration Requirements

The application must make it easy to demonstrate the following during a database course presentation:

### CREATE

Register a user.

Create a project.

### READ

Retrieve projects.

Retrieve a specific project.

Retrieve categories and technologies.

### UPDATE

Edit a project.

Edit a profile.

### DELETE

Delete a project.

### RELATIONSHIPS

Demonstrate:

users → projects

categories → projects

projects ↔ technologies

### JOIN

Provide SQL queries demonstrating how related information is retrieved.

Example:

SELECT project title, creator name, category and technologies.

### CONSTRAINTS

Demonstrate:

* Primary keys
* Foreign keys
* Unique email
* Many-to-many relationship
* NOT NULL fields

---

# 27. Example SQL Demonstration Queries

Include useful SQL examples in the README or a separate documentation file.

Example:

SELECT
p.title,
u.full_name AS creator,
c.name AS category
FROM projects p
JOIN users u ON p.user_id = u.id
JOIN categories c ON p.category_id = c.id;

For technologies:

SELECT
p.title,
t.name AS technology
FROM projects p
JOIN project_technologies pt
ON p.id = pt.project_id
JOIN technologies t
ON pt.technology_id = t.id;

Also provide examples for:

* INSERT
* UPDATE
* DELETE
* WHERE
* ORDER BY
* LIKE
* COUNT
* JOIN

---

# 28. Error Handling

The frontend should never simply fail silently.

Show user-friendly messages for:

* Invalid login
* Duplicate email
* Missing required fields
* Project not found
* Unauthorized project editing
* Database errors
* Network errors

Do not expose raw Python/MySQL error messages to normal users.

---

# 29. README

Create a README explaining:

* What Projektor is
* Features
* Technology stack
* Installation
* MySQL database setup
* Environment variables
* How to run Flask
* How to open the frontend
* Database schema overview
* API endpoints
* Sample login credentials
* Database relationships

Include an ER diagram if practical.

---

# 30. Acceptance Criteria

The MVP is considered complete when:

[ ] MySQL database connects successfully

[ ] Tables are created successfully

[ ] Seed data loads successfully

[ ] User can register

[ ] User can log in

[ ] Passwords are hashed

[ ] User can access dashboard

[ ] User can create a project

[ ] Project is stored in MySQL

[ ] Project appears in Explore

[ ] Project details display creator/category/technologies

[ ] User can edit own project

[ ] User can delete own project

[ ] User cannot edit another user's project

[ ] User cannot delete another user's project

[ ] Search works

[ ] Category filter works

[ ] Status filter works

[ ] Profile can be updated

[ ] Application is responsive

[ ] Errors are handled gracefully

[ ] README exists

[ ] SQL schema exists

[ ] Seed data exists

---

# 31. Important Instruction 

Do not generate the entire project blindly in one enormous step.

Work incrementally.

After completing each major phase:

1. Explain what was created.
2. Explain how it works.
3. Run/test it.
4. Fix errors.
5. Then continue to the next phase.

Prioritize a working MVP over unnecessary features.

Do not replace the agreed technology stack.

Do not introduce unnecessary frameworks.

Do not over-engineer the application.

Keep the code readable because the developer will need to explain the architecture and database design during an academic presentation.

The final application should feel polished, but the underlying implementation should remain understandable.

---

# 32. Final Product Goal

The finished MVP should communicate one simple idea:

> **Projektor gives students a place to make their work visible.**

A visitor should be able to discover projects.

A student should be able to create an account and showcase their work.

The database should be responsible for storing and relating the application's information.

The final system should demonstrate that the developer understands how a web application communicates with a relational database through a Python backend.

**Build the MVP according to this specification.**


