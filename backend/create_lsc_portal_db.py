import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connections

def create_lsc_portal_db():
    """Create the lsc_portal_db database if it doesn't exist"""
    print("\n" + "="*60)
    print("Creating lsc_portal_db Database")
    print("="*60)
    
    try:
        # Connect to MySQL without specifying database
        from django.db import connection
        with connections['online_edu'].cursor() as cursor:
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS lsc_portal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("✓ Database 'lsc_portal_db' created successfully")
            
            # Show databases
            cursor.execute("SHOW DATABASES LIKE 'lsc%'")
            databases = cursor.fetchall()
            print("\n📋 Available LSC Databases:")
            print("-" * 60)
            for db in databases:
                print(f"  - {db[0]}")
            print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating database: {str(e)}")
        return False

if __name__ == '__main__':
    create_lsc_portal_db()
