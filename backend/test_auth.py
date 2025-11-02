"""
Test authentication with the LSCAdmin model
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from lsc_auth.models import LSCAdmin

print("\n" + "=" * 70)
print("Testing LSCAdmin Authentication")
print("=" * 70)

# Get all admins
admins = LSCAdmin.objects.all()
print(f"\nFound {admins.count()} admin(s) in database:\n")

for admin in admins:
    print(f"LSC Code: {admin.lsc_code}")
    print(f"Center Name: {admin.center_name}")
    print(f"Admin Name: {admin.admin_name}")
    print(f"Email: {admin.admin_email}")
    print(f"Mobile: {admin.mobile}")
    print(f"Is Active: {admin.is_active}")
    print(f"Is Admin: {admin.is_admin}")
    print(f"Password Hash: {admin.admin_password[:50]}...")
    print("-" * 70)

# Test authentication
print("\n" + "=" * 70)
print("Testing Authentication:")
print("=" * 70)

test_code = 'LC2101'
test_passwords = ['test123', 'admin123', 'password123']

print(f"\nTesting LSC Code: {test_code}")
print("=" * 70)

try:
    admin = LSCAdmin.objects.get(lsc_code=test_code)
    print(f"✓ Found admin: {admin.admin_name} ({admin.center_name})")
    
    print(f"\nTrying different passwords...")
    for pwd in test_passwords:
        result = admin.check_password(pwd)
        status = "✓ CORRECT" if result else "✗ WRONG"
        print(f"  Password '{pwd}': {status}")
    
    print(f"\n{'='*70}")
    print("Please enter the correct password to test:")
    print("(or press Enter to skip)")
    correct_pwd = input("Password: ").strip()
    
    if correct_pwd:
        if admin.check_password(correct_pwd):
            print(f"\n✓ Authentication SUCCESSFUL for {test_code}!")
            print(f"  Admin: {admin.admin_name}")
            print(f"  Center: {admin.center_name}")
            print(f"  Email: {admin.admin_email}")
        else:
            print(f"\n✗ Authentication FAILED - Wrong password")
    
except LSCAdmin.DoesNotExist:
    print(f"✗ LSC Code '{test_code}' not found")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)
print("\nTo start the server, run:")
print("  python manage.py runserver")
print("\nThen test login at:")
print("  POST http://localhost:8000/api/auth/login/")
print("  Body: {\"lscNumber\": \"LC2101\", \"password\": \"your_password\"}")
print("=" * 70 + "\n")
