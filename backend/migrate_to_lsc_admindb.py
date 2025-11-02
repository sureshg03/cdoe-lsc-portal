"""
Script to migrate portal_applicationsettings table to lsc_admindb database
"""
import MySQLdb
import os
import django
import sys

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def create_database():
    """Create lsc_admindb database if it doesn't exist"""
    print("Creating lsc_admindb database...")
    try:
        # Connect to MySQL without specifying a database
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            port=3306
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS lsc_admindb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✓ Database lsc_admindb created/verified")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return False

def run_migrations():
    """Run portal migrations on lsc_admindb"""
    print("\nRunning migrations on lsc_admindb...")
    try:
        # First migrate Django core apps to lsc_admindb
        print("  - Migrating Django core tables...")
        call_command('migrate', '--database=lsc_admindb', verbosity=2)
        
        # Then migrate portal app
        print("  - Migrating portal app...")
        call_command('migrate', 'portal', '--database=lsc_admindb', verbosity=2)
        
        print("✓ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"✗ Error running migrations: {e}")
        return False

def verify_table():
    """Verify portal_applicationsettings table exists in lsc_admindb"""
    print("\nVerifying table creation...")
    try:
        from django.db import connections
        with connections['lsc_admindb'].cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'portal_applicationsettings'")
            result = cursor.fetchone()
            
            if result:
                print("✓ Table portal_applicationsettings exists in lsc_admindb")
                
                # Show table structure
                cursor.execute("DESCRIBE portal_applicationsettings")
                columns = cursor.fetchall()
                print("\nTable structure:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
                
                return True
            else:
                print("✗ Table not found in lsc_admindb")
                return False
    except Exception as e:
        print(f"✗ Error verifying table: {e}")
        return False

def check_old_tables():
    """Check if portal_applicationsettings exists in old databases"""
    print("\nChecking old database locations...")
    
    databases_to_check = ['default', 'online_edu']
    
    for db_alias in databases_to_check:
        try:
            from django.db import connections
            with connections[db_alias].cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE 'portal_applicationsettings'")
                result = cursor.fetchone()
                
                db_name = connections[db_alias].settings_dict['NAME']
                if result:
                    print(f"  ⚠ Table found in {db_name} - needs cleanup")
                else:
                    print(f"  ✓ No portal tables in {db_name}")
        except Exception as e:
            print(f"  - Error checking {db_alias}: {e}")

def main():
    print("=" * 60)
    print("Portal Table Migration to lsc_admindb")
    print("=" * 60)
    
    # Step 1: Create database
    if not create_database():
        print("\n❌ Failed to create database. Exiting.")
        sys.exit(1)
    
    # Step 2: Run migrations
    if not run_migrations():
        print("\n❌ Failed to run migrations. Exiting.")
        sys.exit(1)
    
    # Step 3: Verify table
    if not verify_table():
        print("\n❌ Table verification failed. Exiting.")
        sys.exit(1)
    
    # Step 4: Check old locations
    check_old_tables()
    
    print("\n" + "=" * 60)
    print("✓ Migration completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Test creating a new admission in the frontend")
    print("2. Verify it saves to lsc_admindb.portal_applicationsettings")
    print("3. If successful, drop old table from lsc_portal_db")
    print("   SQL: USE lsc_portal_db; DROP TABLE portal_applicationsettings;")

if __name__ == '__main__':
    main()
