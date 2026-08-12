-- 03_insert_seed_data.sql
-- This script populates the database with initial sample data.
USE projektor_db;
-- 1. Insert Categories
INSERT INTO categories (name, description)
VALUES (
        'Web Development',
        'Projects related to building websites and web applications.'
    ),
    (
        'Mobile Development',
        'Android and iOS mobile applications.'
    ),
    (
        'Artificial Intelligence',
        'AI models, tools, and applications.'
    ),
    (
        'Machine Learning',
        'Data models and predictive algorithms.'
    ),
    (
        'Data Science',
        'Data analysis, visualization, and big data projects.'
    ),
    (
        'IoT & Embedded Systems',
        'Hardware and software integration projects.'
    ),
    ('Robotics', 'Robotic systems and automation.'),
    (
        'Electronics',
        'Circuit design and hardware projects.'
    ),
    (
        'Cybersecurity',
        'Security tools, audits, and research.'
    ),
    ('Networking', 'Network design and analysis.'),
    (
        'Research',
        'Academic and scientific research papers/projects.'
    ),
    (
        'Design & Creative',
        'UI/UX, graphics, and creative media.'
    ),
    (
        'Business & Entrepreneurship',
        'Business plans and startup ideas.'
    ),
    (
        'Other',
        'Projects that do not fit into other categories.'
    );
-- 2. Insert Technologies
INSERT INTO technologies (name)
VALUES ('HTML'),
    ('CSS'),
    ('JavaScript'),
    ('Python'),
    ('Flask'),
    ('MySQL'),
    ('C++'),
    ('Java'),
    ('PHP'),
    ('Node.js'),
    ('React'),
    ('Arduino'),
    ('ESP32'),
    ('Git'),
    ('GitHub');
-- 3. Insert Users
-- Note: In a real app, password_hash would be an actual bcrypt hash.
-- Using a placeholder hash for demonstration purposes.
INSERT INTO users (
        full_name,
        email,
        password_hash,
        institution,
        program,
        level,
        bio
    )
VALUES (
        'Frank Bediako',
        'frankbediako38@gmail.com',
        '$2b$12$PLACEHOLDERHASH1',
        'University of Energy and Natural Resources',
        'BSc Computer Engineering',
        'Level 300',
        'Passionate about IoT and Embedded Systems.'
    ),
    (
        'Ama Mensah',
        'ama@example.com',
        '$2b$12$PLACEHOLDERHASH2',
        'University of Ghana',
        'BSc Computer Science',
        'Level 200',
        'Web developer and open source contributor.'
    ),
    (
        'John Doe',
        'john@example.com',
        '$2b$12$PLACEHOLDERHASH3',
        'KNUST',
        'BSc Software Engineering',
        'Level 400',
        'Building scalable web applications.'
    ),
    (
        'Jane Smith',
        'jane@example.com',
        '$2b$12$PLACEHOLDERHASH4',
        NULL,
        NULL,
        NULL,
        'Independent learner and creative designer.'
    ),
    (
        'Kwame Appiah',
        'kwame@example.com',
        '$2b$12$PLACEHOLDERHASH5',
        'Ashesi University',
        'BSc Management Information Systems',
        'Level 100',
        'Interested in data and analytics.'
    );
-- 4. Insert Projects
-- Ensure the category_ids and user_ids match the inserted data.
INSERT INTO projects (
        user_id,
        category_id,
        title,
        description,
        status,
        academic_year
    )
VALUES (
        1,
        6,
        'Smart Home Automation System',
        'A low-cost smart home system using ESP32 to control appliances via a web interface.',
        'Completed',
        '2023/2024'
    ),
    (
        2,
        1,
        'Student Expense Tracker',
        'A web application to help students manage their monthly expenses and track their budgets.',
        'In Progress',
        '2024/2025'
    ),
    (
        3,
        14,
        'Campus Navigation System',
        'Software to help freshers navigate around the large campus environment easily.',
        'Completed',
        '2023/2024'
    ),
    (
        1,
        8,
        'Automated Plant Watering System',
        'An Arduino-based system that monitors soil moisture and waters plants automatically.',
        'Completed',
        '2022/2023'
    ),
    (
        4,
        12,
        'Portfolio Website Template',
        'A responsive minimalist portfolio template for creative professionals.',
        'Completed',
        NULL
    );
-- 5. Insert Project Technologies
-- Map projects to technologies based on project_id and technology_id
-- Smart Home (Project 1) uses ESP32 (13), Arduino (12), C++ (7)
INSERT INTO project_technologies (project_id, technology_id)
VALUES (1, 13),
    (1, 12),
    (1, 7);
-- Expense Tracker (Project 2) uses HTML (1), CSS (2), JavaScript (3), Python (4), MySQL (6)
INSERT INTO project_technologies (project_id, technology_id)
VALUES (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 6);
-- Campus Navigation (Project 3) uses JavaScript (3), Python (4), MySQL (6)
INSERT INTO project_technologies (project_id, technology_id)
VALUES (3, 3),
    (3, 4),
    (3, 6);
-- Plant Watering (Project 4) uses Arduino (12), C++ (7)
INSERT INTO project_technologies (project_id, technology_id)
VALUES (4, 12),
    (4, 7);
-- Portfolio Template (Project 5) uses HTML (1), CSS (2), JavaScript (3)
INSERT INTO project_technologies (project_id, technology_id)
VALUES (5, 1),
    (5, 2),
    (5, 3);