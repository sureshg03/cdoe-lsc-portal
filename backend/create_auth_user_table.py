import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connections

def create_auth_user_table():
    """Create minimal auth_user table to support Django auth system"""
    print("\n" + "="*60)
    print("Creating auth_user table in lsc_portal_db")
    print("="*60)
    
    try:
        with connections['default'].cursor() as cursor:
            # Check if table exists
            cursor.execute("SHOW TABLES LIKE 'auth_user'")
            exists = cursor.fetchone()
            
            if exists:
                print("✓ auth_user table already exists")
            else:
                # Create auth_user table
                cursor.execute("""
                    CREATE TABLE auth_user (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        password VARCHAR(128) NOT NULL,
                        last_login DATETIME(6) NULL,
                        is_superuser TINYINT(1) NOT NULL DEFAULT 0,
                        username VARCHAR(150) NOT NULL UNIQUE,
                        first_name VARCHAR(150) NOT NULL DEFAULT '',
                        last_name VARCHAR(150) NOT NULL DEFAULT '',
                        email VARCHAR(254) NOT NULL DEFAULT '',
                        is_staff TINYINT(1) NOT NULL DEFAULT 0,
                        is_active TINYINT(1) NOT NULL DEFAULT 1,
                        date_joined DATETIME(6) NOT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """)
                print("✓ auth_user table created successfully")
            
            # Show all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\n📋 Total tables in lsc_portal_db: {len(tables)}")
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    create_auth_user_table()
