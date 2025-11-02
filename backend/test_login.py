#!/usr/bin/env python
import os
import django
import sys
import requests
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from lsc_auth.models import LSCUser

print("🔍 Checking LSC Users in Database...")
users = LSCUser.objects.all()
print(f"Found {users.count()} users:")
for user in users:
    print(f"  - LSC: {user.lsc_number}, Name: {user.lsc_name}, Active: {user.is_active}")

if users.count() == 0:
    print("❌ No users found! Creating test user...")
    try:
        user = LSCUser.objects.create_user(
            lsc_number='LSC001',
            password='password123',
            lsc_name='Test Counsellor',
            email='test@example.com'
        )
        print(f"✅ Created user: LSC001 / password123")
    except Exception as e:
        print(f"❌ Error creating user: {e}")

print("\n🔍 Testing Login API...")
try:
    response = requests.post(
        'http://localhost:8000/api/auth/login/',
        json={'lscNumber': 'LSC001', 'password': 'password123'},
        headers={'Content-Type': 'application/json'}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ API Error: {e}")
    print("Make sure the Django server is running: python manage.py runserver")