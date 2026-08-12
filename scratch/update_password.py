import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from flask_bcrypt import Bcrypt
from database import get_db_connection

bcrypt = Bcrypt()

def update_password():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    password = "password123"
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    
    query = "UPDATE users SET password_hash = %s WHERE email = 'frankbediako38@gmail.com'"
    cursor.execute(query, (hashed_pw,))
    conn.commit()
    
    print("Password updated successfully!")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    update_password()
