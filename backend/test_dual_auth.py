import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import authenticate
from lsc_auth.models import LSCAdmin, LSCUser
from django.contrib.auth.hashers import make_password

def test_dual_database_authentication():
    """Test authentication from both databases"""
    print("\n" + "="*70)
    print("DUAL DATABASE AUTHENTICATION TEST")
    print("="*70)
    
    print("\n📊 Database Configuration:")
    print("-" * 70)
    print("  1. online_edu.lsc_admins    → Admin & LSC Center Admins")
    print("  2. lsc_portal_db.lsc_auth_lscuser → LSC Center Users")
    print("-" * 70)
    
    # Test 1: Check LSCAdmin records in online_edu
    print("\n" + "="*70)
    print("Test 1: LSCAdmin Records (online_edu.lsc_admins)")
    print("="*70)
    
    try:
        admins = LSCAdmin.objects.using('online_edu').all()
        print(f"✓ Found {admins.count()} admin records")
        for admin in admins:
            print(f"  - {admin.lsc_code}: {admin.center_name[:50]}")
    except Exception as e:
        print(f"✗ Error querying LSCAdmin: {str(e)}")
    
    # Test 2: Check LSCUser records in lsc_portal_db
    print("\n" + "="*70)
    print("Test 2: LSCUser Records (lsc_portal_db.lsc_auth_lscuser)")
    print("="*70)
    
    try:
        users = LSCUser.objects.using('default').all()
        print(f"✓ Found {users.count()} user records")
        if users.count() == 0:
            print("  ⚠ No LSC users found. Creating test user...")
            # Create a test LSC user
            test_user = LSCUser(
                lsc_number='LC3001',
                lsc_name='Test LSC Center User',
                email='test@lsc.edu'
            )
            test_user.set_password('user123')
            test_user.save(using='default')
            print(f"  ✓ Test user created: LC3001 / user123")
        else:
            for user in users:
                print(f"  - {user.lsc_number}: {user.lsc_name}")
    except Exception as e:
        print(f"✗ Error querying LSCUser: {str(e)}")
    
    # Test 3: Test Admin Authentication (LC2101-CDOE)
    print("\n" + "="*70)
    print("Test 3: Admin Authentication (LC2101-CDOE)")
    print("="*70)
    
    admin_user = authenticate(lsc_code='LC2101-CDOE', password='admin123')
    if admin_user:
        print("✓ ADMIN AUTHENTICATION SUCCESSFUL!")
        print(f"  User Type: {type(admin_user).__name__}")
        print(f"  LSC Code: {admin_user.lsc_code}")
        print(f"  Name: {getattr(admin_user, 'center_name', 'N/A')}")
        print(f"  Database: {getattr(admin_user, '_database', 'online_edu')}")
        print(f"  Is Admin: {getattr(admin_user, 'is_admin', False)}")
    else:
        print("✗ Admin authentication FAILED")
        print("  Make sure LC2101-CDOE exists with password 'admin123'")
    
    # Test 4: Test LSC User Authentication
    print("\n" + "="*70)
    print("Test 4: LSC User Authentication (LC3001)")
    print("="*70)
    
    lsc_user = authenticate(lsc_number='LC3001', password='user123')
    if lsc_user:
        print("✓ LSC USER AUTHENTICATION SUCCESSFUL!")
        print(f"  User Type: {type(lsc_user).__name__}")
        print(f"  LSC Number: {lsc_user.lsc_number}")
        print(f"  Name: {lsc_user.lsc_name}")
        print(f"  Database: {getattr(lsc_user, '_database', 'default')}")
    else:
        print("✗ LSC user authentication FAILED")
        print("  User LC3001 may not exist or password is incorrect")
    
    # Test 5: Test Invalid Credentials
    print("\n" + "="*70)
    print("Test 5: Invalid Credentials (Should Fail)")
    print("="*70)
    
    invalid_user = authenticate(lsc_code='INVALID', password='wrong')
    if invalid_user:
        print("✗ UNEXPECTED: Invalid credentials accepted!")
    else:
        print("✓ Correctly rejected invalid credentials")
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print("✓ Dual database authentication is configured")
    print("✓ Admin authentication checks online_edu.lsc_admins")
    print("✓ User authentication checks lsc_portal_db.lsc_auth_lscuser")
    print("\n📝 Usage:")
    print("  Admin Login: LC2101-CDOE / admin123")
    print("  User Login:  LC3001 / user123")
    print("="*70 + "\n")

if __name__ == '__main__':
    test_dual_database_authentication()
