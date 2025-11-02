import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from lsc_auth.models import LSCUser

def create_test_lsc_user():
    """Create a test LSC user for testing"""
    print("\n" + "="*60)
    print("Creating Test LSC User")
    print("="*60)
    
    try:
        # Check if user already exists
        existing = LSCUser.objects.using('default').filter(lsc_number='LC3001').first()
        if existing:
            print(f"User already exists: {existing.lsc_number}")
            print("Updating password to 'user123'...")
            existing.set_password('user123')
            existing.save(using='default')
            print("✓ Password updated!")
        else:
            # Create new user
            user = LSCUser(
                lsc_number='LC3001',
                lsc_name='Salem LSC Center',
                email='salem@lsc.periyar.edu'
            )
            user.set_password('user123')
            user.save(using='default')
            print("✓ Test LSC user created!")
        
        print("\n📋 User Details:")
        user = LSCUser.objects.using('default').get(lsc_number='LC3001')
        print(f"  LSC Number: {user.lsc_number}")
        print(f"  LSC Name: {user.lsc_name}")
        print(f"  Email: {user.email}")
        print(f"  Is Active: {user.is_active}")
        print(f"  Password: user123")
        print("\n✓ You can now login with:")
        print(f"  Username: LC3001")
        print(f"  Password: user123")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_test_lsc_user()
