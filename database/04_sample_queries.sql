-- 04_sample_queries.sql
-- This file contains example queries demonstrating important database operations.
-- It can be used during the database course presentation to show how SQL interacts with Projektor.

USE projektor_db;

-- ==========================================
-- 1. BASIC SELECT & FILTERING (WHERE, LIKE)
-- ==========================================

-- Select all users (excluding passwords for safety in presentation)
SELECT id, full_name, email, institution, program 
FROM users;

-- Select a specific user by email
SELECT full_name, program 
FROM users 
WHERE email = 'frankbediako38@gmail.com';

-- Search projects using LIKE (e.g., finding projects with "System" in the title)
SELECT title, status 
FROM projects 
WHERE title LIKE '%System%';


-- ==========================================
-- 2. SORTING & GROUPING (ORDER BY, COUNT, GROUP BY)
-- ==========================================

-- Count total number of projects in the database
SELECT COUNT(*) AS total_projects 
FROM projects;

-- Count projects by status and order them
SELECT status, COUNT(*) AS project_count 
FROM projects 
GROUP BY status 
ORDER BY project_count DESC;

-- List all categories and the number of projects in each
SELECT c.name AS category_name, COUNT(p.id) AS number_of_projects
FROM categories c
LEFT JOIN projects p ON c.id = p.category_id
GROUP BY c.id, c.name
ORDER BY number_of_projects DESC;


-- ==========================================
-- 3. JOINS (Retrieving related data)
-- ==========================================

-- Retrieve projects along with their creator's name and category
SELECT 
    p.title AS project_title,
    p.status,
    u.full_name AS creator,
    c.name AS category
FROM projects p
JOIN users u ON p.user_id = u.id
JOIN categories c ON p.category_id = c.id;

-- Retrieve all technologies used in a specific project (e.g., Project ID 1)
SELECT 
    p.title AS project_title,
    t.name AS technology_used
FROM projects p
JOIN project_technologies pt ON p.id = pt.project_id
JOIN technologies t ON pt.technology_id = t.id
WHERE p.id = 1;


-- ==========================================
-- 4. INSERT, UPDATE, DELETE (CRUD Operations)
-- ==========================================

-- INSERT: Add a new dummy project for user 1
INSERT INTO projects (user_id, category_id, title, description, status) 
VALUES (1, 1, 'Dummy Web App', 'A temporary project to demonstrate INSERT.', 'In Progress');

-- UPDATE: Change the status of the newly created project
UPDATE projects 
SET status = 'Completed' 
WHERE title = 'Dummy Web App';

-- DELETE: Remove the dummy project
DELETE FROM projects 
WHERE title = 'Dummy Web App';
