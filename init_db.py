import os
from dotenv import load_dotenv
import pyodbc
from models import db, User, MacroMaster
from datetime import datetime
import pandas as pd

# Load environment variables
load_dotenv()

def recreate_database():
    """Recreate the database from scratch"""
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    
    # Connect to master database
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};'
        f'DATABASE=master;UID={username};PWD={password}',
        autocommit=True
    )
    
    cursor = conn.cursor()
    
    # Drop database if exists
    print(f"Dropping database {database} if exists...")
    cursor.execute(f"""
        IF EXISTS (SELECT name FROM sys.databases WHERE name = N'{database}')
        BEGIN
            ALTER DATABASE [{database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
            DROP DATABASE [{database}];
        END
    """)
    
    # Create database
    print(f"Creating database {database}...")
    cursor.execute(f"CREATE DATABASE [{database}]")
    print(f"Database {database} created successfully!")
    
    cursor.close()
    conn.close()

def init_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create default admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create some sample macro master data
        sample_macros = [
            ('GDP Growth', '202301'),
            ('Inflation Rate', '202301'),
            ('Interest Rate', '202301'),
            ('Exchange Rate', '202301'),
            ('GDP Growth', '202302'),
            ('Inflation Rate', '202302'),
            ('Interest Rate', '202302'),
            ('Exchange Rate', '202302'),
        ]
        
        for name, period in sample_macros:
            macro = MacroMaster(
                macro_name=name,
                period=pd.to_datetime(period, format='%Y%m').date()
            )
            db.session.add(macro)
        
        db.session.commit()

if __name__ == '__main__':
    from flask import Flask
    
    # Create Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}/{os.getenv('DB_NAME')}?driver=ODBC+Driver+17+for+SQL+Server"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        # Recreate database
        recreate_database()
        
        # Initialize database
        init_db()
