import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from lsc_auth.models import LSCAdmin
from django.db import connection
from django.contrib.auth.hashers import make_password

def test_database_connection():
    """Test database connection and table structure"""
    print("\n" + "="*60)
    print("Testing Database Connection to online_edu.lsc_admins")
    print("="*60)
    
    try:
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"✓ Connected to database: {db_name}")
            
            # Check if table exists
            cursor.execute("SHOW TABLES LIKE 'lsc_admins'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                print("✓ Table 'lsc_admins' exists")
                
                # Show table structure
                cursor.execute("DESCRIBE lsc_admins")
                columns = cursor.fetchall()
                print("\n📋 Table Structure:")
                print("-" * 60)
                for col in columns:
                    print(f"  {col[0]:<20} {col[1]:<20} {col[2]}")
                print("-" * 60)
                
                # Count records
                cursor.execute("SELECT COUNT(*) FROM lsc_admins")
                count = cursor.fetchone()[0]
                print(f"\n📊 Total records in lsc_admins: {count}")
                
                # Show sample data (first 5 records, limited fields for security)
                if count > 0:
                    cursor.execute("SELECT id, lsc_code, center_name, admin_name, is_active FROM lsc_admins LIMIT 5")
                    records = cursor.fetchall()
                    print("\n📄 Sample Records (first 5):")
                    print("-" * 60)
                    for record in records:
                        print(f"  ID: {record[0]}, LSC: {record[1]}, Center: {record[2][:30]}..., Admin: {record[3]}, Active: {record[4]}")
                    print("-" * 60)
                    
                    # Check for LC2101-CDOE admin
                    cursor.execute("SELECT id, lsc_code, center_name, admin_name FROM lsc_admins WHERE lsc_code LIKE '%LC2101%' OR lsc_code LIKE '%CDOE%'")
                    cdoe_record = cursor.fetchone()
                    if cdoe_record:
                        print(f"\n✓ Main Admin (LC2101-CDOE) found:")
                        print(f"  ID: {cdoe_record[0]}")
                        print(f"  LSC Code: {cdoe_record[1]}")
                        print(f"  Center: {cdoe_record[2]}")
                        print(f"  Admin: {cdoe_record[3]}")
                    else:
                        print("\n⚠ Warning: Main Admin (LC2101-CDOE) not found in database")
                
            else:
                print("✗ Table 'lsc_admins' does not exist!")
                print("\nAvailable tables:")
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                for table in tables:
                    print(f"  - {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Database Error: {str(e)}")
        return False

def test_lsc_admin_model():
    """Test LSCAdmin model functionality"""
    print("\n" + "="*60)
    print("Testing LSCAdmin Model")
    print("="*60)
    
    try:
        # Try to fetch all admins
        admins = LSCAdmin.objects.all()
        print(f"\n✓ Successfully queried LSCAdmin model")
        print(f"  Total admins found: {admins.count()}")
        
        if admins.count() > 0:
            print("\n📋 LSC Admins:")
            print("-" * 60)
            for admin in admins[:5]:  # Show first 5
                print(f"  LSC: {admin.lsc_code:<15} Center: {admin.center_name[:40]}")
            print("-" * 60)
            
            # Test authentication with first admin
            first_admin = admins.first()
            print(f"\n🔐 Testing password check for: {first_admin.lsc_code}")
            # Note: We can't test actual password without knowing it
            print(f"  Password field exists: {bool(first_admin.admin_password)}")
            print(f"  Is active: {first_admin.is_active}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Model Error: {str(e)}")
        return False

def create_test_admin():
    """Create a test admin if LC2101-CDOE doesn't exist"""
    print("\n" + "="*60)
    print("Creating Test Admin (LC2101-CDOE)")
    print("="*60)
    
    try:
        # Check if admin already exists
        existing = LSCAdmin.objects.filter(lsc_code='LC2101-CDOE').first()
        if existing:
            print(f"✓ Admin already exists: {existing.lsc_code}")
            return existing
        
        # Create new admin with hashed password
        admin = LSCAdmin(
            lsc_code='LC2101-CDOE',
            center_name='Centre for Distance and Online Education',
            admin_email='admin@cdoe.periyar.edu',
            admin_password=make_password('admin123'),  # Default password: admin123
            admin_name='CDOE Administrator',
            mobile='9876543210',
            address='Periyar University Campus',
            district='Salem',
            state='Tamil Nadu',
            pincode='636011',
            is_active=True,
            created_by='system'
        )
        admin.save()
        
        print("✓ Test admin created successfully!")
        print(f"  LSC Code: {admin.lsc_code}")
        print(f"  Center: {admin.center_name}")
        print(f"  Email: {admin.admin_email}")
        print(f"  Default Password: admin123")
        print("\n⚠ IMPORTANT: Please change the password after first login!")
        
        return admin
        
    except Exception as e:
        print(f"\n✗ Error creating admin: {str(e)}")
        return None

if __name__ == '__main__':
    print("\n" + "="*60)
    print("LSC Admin Database Test Script")
    print("="*60)
    
    # Test 1: Database connection
    db_ok = test_database_connection()
    
    if db_ok:
        # Test 2: Model functionality
        model_ok = test_lsc_admin_model()
        
        # Test 3: Create test admin if needed
        if model_ok:
            print("\n" + "="*60)
            print("Do you want to create a test admin (LC2101-CDOE)?")
            print("="*60)
            response = input("Create test admin? (y/n): ").lower()
            if response == 'y':
                create_test_admin()
    
    print("\n" + "="*60)
    print("Test Complete")
    print("="*60 + "\n")
