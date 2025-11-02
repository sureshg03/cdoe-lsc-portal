"""
Test script to verify connection to online_edu database and lsc_admins table
Run this from the backend directory: python test_lsc_admin_connection.py
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from lsc_auth.models import LSCAdmin
from django.db import connection
from django.contrib.auth.hashers import make_password

def test_database_connection():
    """Test database connection"""
    print("=" * 60)
    print("Testing Database Connection...")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"✓ Connected to database: {db_name}")
            
            # Check if lsc_admins table exists
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = 'lsc_admins'
            """, [db_name])
            
            table_exists = cursor.fetchone()[0]
            if table_exists:
                print(f"✓ Table 'lsc_admins' exists")
            else:
                print(f"✗ Table 'lsc_admins' does not exist")
                print("\nCreating lsc_admins table...")
                create_table()
                
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        return False
    
    return True

def create_table():
    """Create lsc_admins table if it doesn't exist"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lsc_admins (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    lsc_code VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    lsc_name VARCHAR(255),
                    email VARCHAR(255),
                    is_active BOOLEAN DEFAULT TRUE,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    last_login TIMESTAMP NULL,
                    INDEX idx_lsc_code (lsc_code),
                    INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("✓ Table 'lsc_admins' created successfully")
    except Exception as e:
        print(f"✗ Error creating table: {e}")

def list_admins():
    """List all LSC admins"""
    print("\n" + "=" * 60)
    print("LSC Admins in Database:")
    print("=" * 60)
    
    try:
        admins = LSCAdmin.objects.all()
        
        if admins.exists():
            print(f"\nFound {admins.count()} admin(s):\n")
            for admin in admins:
                print(f"  ID: {admin.id}")
                print(f"  LSC Code: {admin.lsc_code}")
                print(f"  LSC Name: {admin.lsc_name or 'Not Set'}")
                print(f"  Email: {admin.email or 'Not Set'}")
                print(f"  Is Admin: {admin.is_admin}")
                print(f"  Is Active: {admin.is_active}")
                print(f"  Last Login: {admin.last_login or 'Never'}")
                print(f"  Password (hashed): {admin.password[:50]}...")
                print("-" * 60)
        else:
            print("\nNo admins found in database.")
            print("\nCreating default admin accounts...")
            create_default_admins()
            
    except Exception as e:
        print(f"✗ Error listing admins: {e}")

def create_default_admins():
    """Create default admin accounts for testing"""
    default_admins = [
        {
            'lsc_code': 'LC2101',
            'password': 'admin123',  # Will be hashed
            'lsc_name': 'Centre for Distance and Online Education (CDOE)',
            'email': 'cdoe@periyaruniversity.ac.in',
            'is_admin': True,
            'is_active': True
        },
        {
            'lsc_code': 'LC2102',
            'password': 'lsc123',  # Will be hashed
            'lsc_name': 'Salem LSC Center',
            'email': 'salem@periyaruniversity.ac.in',
            'is_admin': False,
            'is_active': True
        },
        {
            'lsc_code': 'LC2103',
            'password': 'lsc123',  # Will be hashed
            'lsc_name': 'Erode LSC Center',
            'email': 'erode@periyaruniversity.ac.in',
            'is_admin': False,
            'is_active': True
        }
    ]
    
    try:
        for admin_data in default_admins:
            # Check if already exists
            if LSCAdmin.objects.filter(lsc_code=admin_data['lsc_code']).exists():
                print(f"  ⚠ {admin_data['lsc_code']} already exists, skipping...")
                continue
            
            # Create new admin with hashed password
            admin = LSCAdmin(
                lsc_code=admin_data['lsc_code'],
                password=make_password(admin_data['password']),  # Hash the password
                lsc_name=admin_data['lsc_name'],
                email=admin_data['email'],
                is_admin=admin_data['is_admin'],
                is_active=admin_data['is_active']
            )
            admin.save()
            print(f"  ✓ Created admin: {admin_data['lsc_code']} (Password: {admin_data['password']})")
        
        print("\n✓ Default admin accounts created successfully!")
        print("\nYou can now login with:")
        print("  - LSC Code: LC2101, Password: admin123 (Admin)")
        print("  - LSC Code: LC2102, Password: lsc123")
        print("  - LSC Code: LC2103, Password: lsc123")
        
    except Exception as e:
        print(f"✗ Error creating default admins: {e}")

def test_authentication():
    """Test authentication with sample credentials"""
    print("\n" + "=" * 60)
    print("Testing Authentication:")
    print("=" * 60)
    
    test_cases = [
        ('LC2101', 'admin123'),
        ('LC2102', 'lsc123'),
        ('LC2103', 'wrongpassword'),  # Should fail
    ]
    
    for lsc_code, password in test_cases:
        print(f"\nTesting: {lsc_code} / {password}")
        try:
            admin = LSCAdmin.objects.get(lsc_code=lsc_code)
            if admin.check_password(password):
                print(f"  ✓ Authentication successful for {lsc_code}")
            else:
                print(f"  ✗ Authentication failed for {lsc_code} (wrong password)")
        except LSCAdmin.DoesNotExist:
            print(f"  ✗ LSC Code {lsc_code} not found")
        except Exception as e:
            print(f"  ✗ Error: {e}")

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("LSC Admin Database Test Script")
    print("=" * 60)
    
    if test_database_connection():
        list_admins()
        test_authentication()
        
        print("\n" + "=" * 60)
        print("Test Complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Start the Django server: python manage.py runserver")
        print("2. Test login at: http://localhost:8000/api/auth/login/")
        print("3. Use LSC Code and Password from above")
        print("=" * 60 + "\n")
