from app import app, db

def check_macro_master():
    with app.app_context():
        result = db.engine.execute("""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'macro_master'
        """)
        
        print("\nMacro Master columns:")
        for row in result:
            print(row)

if __name__ == '__main__':
    check_macro_master()
