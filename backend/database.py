import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path, override=True)

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    The caller is responsible for closing the connection and its cursor.
    """
    try:
        host = os.getenv("DB_HOST", "localhost")
        print(f"Connecting to DB at {host}...", flush=True)
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "projektor_db"),
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )
        print("Connected!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL Database: {err}")
        raise err

if __name__ == '__main__':
    # Test connection when this file is run directly
    conn = get_db_connection()
    if conn and conn.is_connected():
        print(f"SUCCESS: Python successfully connected to MySQL database '{os.getenv('DB_NAME')}'")
        
        # Test a simple query to prove it works
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as user_count FROM users")
        result = cursor.fetchone()
        print(f"Verified Database Content: Found {result['user_count']} users in the database.")
        
        cursor.close()
        conn.close()
    else:
        print("FAILED: Python could not connect to MySQL.")
