from app import app, db
from models import MacroValue
from sqlalchemy import text

def recreate_macro_values():
    with app.app_context():
        # Drop the table using SQLAlchemy
        MacroValue.__table__.drop(db.engine, checkfirst=True)
        
        # Create new table
        db.engine.execute("""
            CREATE TABLE macro_values (
                periode CHAR(6) NOT NULL, 
                macro_variable_id INTEGER NOT NULL, 
                macro_variable_name VARCHAR(255) NOT NULL, 
                date_regresi DATE NOT NULL, 
                value FLOAT NOT NULL, 
                created_at DATETIME NULL, 
                PRIMARY KEY (periode, macro_variable_id, date_regresi), 
                FOREIGN KEY(periode, macro_variable_id) 
                    REFERENCES macro_master (periode, macro_variable_id)
            )
        """)
        
        print("Table macro_values has been recreated successfully!")

if __name__ == '__main__':
    recreate_macro_values()
