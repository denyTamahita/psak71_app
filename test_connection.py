import os
from dotenv import load_dotenv
import pyodbc
import time

# Load environment variables
load_dotenv()

def test_connection():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    
    print(f"Testing connection to {server}...")
    
    try:
        # Try to connect to master database first
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            'DATABASE=master;'
            f'UID={username};'
            f'PWD={password};'
            'Trusted_Connection=no;'
            'TrustServerCertificate=yes;'
            'Connection Timeout=30'
        )
        
        conn = pyodbc.connect(conn_str, autocommit=True)
        cursor = conn.cursor()
        
        print("Successfully connected to master database!")
        
        # Test if our database exists
        cursor.execute(f"SELECT database_id FROM sys.databases WHERE Name = '{database}'")
        result = cursor.fetchone()
        
        if result:
            print(f"Database {database} exists!")
            
            # Try to connect to our database
            conn.close()
            conn_str = conn_str.replace('DATABASE=master', f'DATABASE={database}')
            conn = pyodbc.connect(conn_str, autocommit=True)
            cursor = conn.cursor()
            
            # Test a simple query
            cursor.execute("SELECT COUNT(*) FROM sys.tables")
            count = cursor.fetchone()[0]
            print(f"Successfully connected to {database}! Found {count} tables.")
        else:
            print(f"Database {database} does not exist!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nConnection string used:")
        print(conn_str.replace(password, '*****'))  # Hide password in output
        return False
    
    return True

if __name__ == '__main__':
    max_retries = 3
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        print(f"\nAttempt {attempt + 1} of {max_retries}")
        if test_connection():
            break
        elif attempt < max_retries - 1:
            print(f"\nRetrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
