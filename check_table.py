from app import app, db

def check_tables():
    with app.app_context():
        # Get table info
        result = db.engine.execute("""
            SELECT 
                c.name 'Column Name',
                t.Name 'Data type',
                c.max_length 'Max Length',
                c.precision ,
                c.scale ,
                c.is_nullable
            FROM sys.columns c
            INNER JOIN sys.types t ON c.user_type_id = t.user_type_id
            WHERE c.object_id = OBJECT_ID('macro_master')
        """)
        
        print("\nMacro Master columns:")
        for row in result:
            print(row)
            
        result = db.engine.execute("""
            SELECT 
                c.name 'Column Name',
                t.Name 'Data type',
                c.max_length 'Max Length',
                c.precision ,
                c.scale ,
                c.is_nullable
            FROM sys.columns c
            INNER JOIN sys.types t ON c.user_type_id = t.user_type_id
            WHERE c.object_id = OBJECT_ID('macro_values')
        """)
        
        print("\nMacro Values columns:")
        for row in result:
            print(row)

if __name__ == '__main__':
    check_tables()
