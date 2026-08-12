-- 05_test_queries.sql
-- This script contains queries designed to verify that the database is functioning correctly,
-- and that all relationships (One-to-Many, Many-to-Many) are properly maintained.

USE projektor_db;

-- 1. Test basic counts to ensure seed data loaded
SELECT 'Users Count' AS Test, COUNT(*) AS Result FROM users
UNION
SELECT 'Projects Count', COUNT(*) FROM projects
UNION
SELECT 'Categories Count', COUNT(*) FROM categories
UNION
SELECT 'Technologies Count', COUNT(*) FROM technologies;

-- 2. Test Many-to-Many Relationship: List all projects and an aggregated list of their technologies
SELECT 
    p.title AS project_title,
    GROUP_CONCAT(t.name SEPARATOR ', ') AS technologies_used
FROM projects p
LEFT JOIN project_technologies pt ON p.id = pt.project_id
LEFT JOIN technologies t ON pt.technology_id = t.id
GROUP BY p.id;

-- 3. Test One-to-Many Relationships: Projects with Categories and Users
SELECT 
    p.id AS project_id,
    p.title,
    c.name AS category_name,
    u.full_name AS author_name,
    u.institution
FROM projects p
JOIN categories c ON p.category_id = c.id
JOIN users u ON p.user_id = u.id;

-- 4. Test Filtering logic (which backend will use)
-- e.g., Filter for "Completed" projects only
SELECT title, status 
FROM projects 
WHERE status = 'Completed';

-- 5. Test Search logic (which backend will use)
-- e.g., Search for projects related to "Web" or "App"
SELECT title, description 
FROM projects 
WHERE title LIKE '%App%' OR description LIKE '%web%';
