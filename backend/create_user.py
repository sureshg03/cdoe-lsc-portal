#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()

from lsc_auth.models import LSCUser

# Create test user
try:
    user = LSCUser.objects.create_user(
        lsc_number='LSC001',
        password='password123',
        lsc_name='Test Counsellor',
        email='test@example.com'
    )
    print(f"✅ Created LSC User:")
    print(f"   LSC Number: {user.lsc_number}")
    print(f"   Password: password123")
    print(f"   Name: {user.lsc_name}")
except Exception as e:
    print(f"Error creating user: {e}")