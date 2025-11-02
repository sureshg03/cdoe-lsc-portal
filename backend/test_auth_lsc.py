import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import authenticate
from lsc_auth.models import LSCAdmin

def test_authentication(lsc_code, password):
    """Test authentication with given credentials"""
    print(f"\n{'='*60}")
    print(f"Testing Authentication for: {lsc_code}")
    print('='*60)
    
    try:
        # Authenticate using the LSCAdminAuthBackend
        user = authenticate(lsc_code=lsc_code, password=password)
        
        if user:
            print("✓ Authentication SUCCESSFUL!")
            print(f"\n📋 User Details:")
            print(f"  ID: {user.id}")
            print(f"  LSC Code: {user.lsc_code}")
            print(f"  Center Name: {user.center_name}")
            print(f"  Admin Name: {user.admin_name}")
            print(f"  Email: {user.admin_email}")
            print(f"  Mobile: {user.mobile}")
            print(f"  Is Active: {user.is_active}")
            print(f"  Is Admin: {user.is_admin}")
            return True
        else:
            print("✗ Authentication FAILED!")
            print("  Invalid LSC Code or Password")
            return False
            
    except Exception as e:
        print(f"✗ Authentication ERROR: {str(e)}")
        return False

def check_password_hash(lsc_code):
    """Check what type of password hash is stored"""
    print(f"\n{'='*60}")
    print(f"Checking Password Hash for: {lsc_code}")
    print('='*60)
    
    try:
        admin = LSCAdmin.objects.get(lsc_code=lsc_code)
        password_hash = admin.admin_password
        
        print(f"Password Hash: {password_hash[:50]}...")
        print(f"Length: {len(password_hash)}")
        
        if password_hash.startswith('pbkdf2_sha256$'):
            print("Type: Django PBKDF2 SHA256 (Secure)")
        elif password_hash.startswith('bcrypt$'):
            print("Type: BCrypt (Secure)")
        elif password_hash.startswith('argon2'):
            print("Type: Argon2 (Secure)")
        else:
            print("Type: Plain text or unknown hash (INSECURE)")
            print("⚠ WARNING: Password should be hashed for security!")
        
    except LSCAdmin.DoesNotExist:
        print(f"✗ Admin with LSC code '{lsc_code}' not found")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("LSC Authentication Test")
    print("="*60)
    
    # Get all LSC codes
    print("\n📋 Available LSC Codes:")
    print("-" * 60)
    admins = LSCAdmin.objects.all()
    for admin in admins:
        print(f"  - {admin.lsc_code} ({admin.center_name[:40]}...)")
    print("-" * 60)
    
    # Test authentication
    print("\n" + "="*60)
    print("Test Authentication")
    print("="*60)
    
    lsc_code = input("\nEnter LSC Code (e.g., LC2101-CDOE): ").strip()
    
    if not lsc_code:
        print("No LSC code entered. Using default: LC2101-CDOE")
        lsc_code = "LC2101-CDOE"
    
    # Check password hash type
    check_password_hash(lsc_code)
    
    # Test authentication
    password = input(f"\nEnter Password for {lsc_code}: ").strip()
    
    if password:
        test_authentication(lsc_code, password)
    else:
        print("\n⚠ No password entered. Skipping authentication test.")
    
    print("\n" + "="*60)
    print("Test Complete")
    print("="*60 + "\n")
