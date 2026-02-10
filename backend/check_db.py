import sqlite3
import os

# Connect to the SQLite database
db_path = "./todo_local_test.db"  # This is the path used in start_server.py
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if users table exists and has data
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:", tables)
    
    # Check users table if it exists
    if ('user',) in tables or ('users',) in tables:
        cursor.execute("SELECT * FROM user;")
        users = cursor.fetchall()
        print("Users in database:", users)
        
        # Show column names
        cursor.execute("PRAGMA table_info(user);")
        columns = cursor.fetchall()
        print("User table structure:", columns)
    
    conn.close()
else:
    print(f"Database file {db_path} does not exist")