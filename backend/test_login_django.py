#!/usr/bin/env python
import os
import django
import sys
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.test import Client
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

print("\n🔍 Testing Login API with Django test client...")
client = Client()

# Test the login endpoint
response = client.post(
    '/api/auth/login/',
    json.dumps({'lscNumber': 'LSC001', 'password': 'password123'}),
    content_type='application/json'
)

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.get('Content-Type')}")

if response.status_code == 200:
    print("✅ Login successful!")
    print("Response data:", response.json())
else:
    print("❌ Login failed!")
    # Print the HTML content to see the actual error
    content = response.content.decode()
    if 'error' in content.lower() or 'invalid' in content.lower():
        # Try to extract error message from HTML
        import re
        error_match = re.search(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL)
        if error_match:
            print("Error details:", error_match.group(1).strip())
        else:
            print("HTML content (first 500 chars):", content[:500])
    else:
        print("HTML content (first 500 chars):", content[:500])