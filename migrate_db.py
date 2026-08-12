import mysql.connector

# Local connection
local_conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='',
    database='projektor_db'
)

# Remote connection
remote_conn = mysql.connector.connect(
    host='gateway01.eu-central-1.prod.aws.tidbcloud.com',
    port=4000,
    user='a2ZDETvXFaGrDio.root',
    password='wesj6lg1i6d0Leaf',
    database='projektor_db',
    ssl_verify_cert=True,
    ssl_verify_identity=True
)

local_cursor = local_conn.cursor(dictionary=True)
remote_cursor = remote_conn.cursor()

# 1. Create tables on remote if they don't exist
local_cursor.execute("SHOW TABLES")
tables = [t[list(t.keys())[0]] for t in local_cursor.fetchall()]

# Disable foreign key checks temporarily on remote to avoid order issues during creation
remote_cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

for table in tables:
    local_cursor.execute(f"SHOW CREATE TABLE {table}")
    create_stmt = local_cursor.fetchone()['Create Table']
    
    # We must replace CREATE TABLE with CREATE TABLE IF NOT EXISTS just in case
    # or just DROP it first
    # remote_cursor.execute(f"DROP TABLE IF EXISTS {table}")
    try:
        remote_cursor.execute(create_stmt)
        remote_conn.commit()
    except mysql.connector.Error as err:
        if err.errno == 1050:
            pass # Table already exists
        else:
            raise err

remote_cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
print("Schema created remotely.")

# 2. Migrate Users
local_cursor.execute("SELECT * FROM users")
users = local_cursor.fetchall()
for u in users:
    if u:
        cols = u.keys()
        vals = [u[col] for col in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        remote_cursor.execute(f"INSERT IGNORE INTO users ({', '.join(cols)}) VALUES ({placeholders})", vals)
remote_conn.commit()
print(f"Migrated {len(users)} users.")

# 3. Migrate Categories
local_cursor.execute("SELECT * FROM categories")
categories = local_cursor.fetchall()
for c in categories:
    if c:
        cols = c.keys()
        vals = [c[col] for col in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        remote_cursor.execute(f"INSERT IGNORE INTO categories ({', '.join(cols)}) VALUES ({placeholders})", vals)
remote_conn.commit()
print(f"Migrated {len(categories)} categories.")

# 4. Migrate Technologies
local_cursor.execute("SELECT * FROM technologies")
technologies = local_cursor.fetchall()
for t in technologies:
    if t:
        cols = t.keys()
        vals = [t[col] for col in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        remote_cursor.execute(f"INSERT IGNORE INTO technologies ({', '.join(cols)}) VALUES ({placeholders})", vals)
remote_conn.commit()
print(f"Migrated {len(technologies)} technologies.")

# 5. Migrate Projects
local_cursor.execute("SELECT * FROM projects")
projects = local_cursor.fetchall()
for p in projects:
    if p:
        cols = p.keys()
        vals = [p[col] for col in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        remote_cursor.execute(f"INSERT IGNORE INTO projects ({', '.join(cols)}) VALUES ({placeholders})", vals)
remote_conn.commit()
print(f"Migrated {len(projects)} projects.")

# 6. Migrate Project Technologies
local_cursor.execute("SELECT * FROM project_technologies")
project_technologies = local_cursor.fetchall()
for pt in project_technologies:
    if pt:
        cols = pt.keys()
        vals = [pt[col] for col in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        remote_cursor.execute(f"INSERT IGNORE INTO project_technologies ({', '.join(cols)}) VALUES ({placeholders})", vals)
remote_conn.commit()
print(f"Migrated {len(project_technologies)} project_technologies.")

# 7. Migrate Comments
local_cursor.execute("SELECT * FROM comments")
comments = local_cursor.fetchall()
for c in comments:
    if c:
        cols = c.keys()
        vals = [c[col] for col in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        remote_cursor.execute(f"INSERT IGNORE INTO comments ({', '.join(cols)}) VALUES ({placeholders})", vals)
remote_conn.commit()
print(f"Migrated {len(comments)} comments.")

# 8. Migrate Likes
local_cursor.execute("SELECT * FROM likes")
likes = local_cursor.fetchall()
for l in likes:
    if l:
        cols = l.keys()
        vals = [l[col] for col in cols]
        placeholders = ", ".join(["%s"] * len(cols))
        remote_cursor.execute(f"INSERT IGNORE INTO likes ({', '.join(cols)}) VALUES ({placeholders})", vals)
remote_conn.commit()
print(f"Migrated {len(likes)} likes.")

print("Migration completed successfully!")

local_cursor.close()
local_conn.close()
remote_cursor.close()
remote_conn.close()
