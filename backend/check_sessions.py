#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(__file__))
django.setup()

from portal.models import ApplicationSettings

def check_sessions():
    sessions = ApplicationSettings.objects.all()
    print(f"Found {sessions.count()} admission sessions:")
    print("-" * 60)

    for session in sessions:
        print(f"ID: {session.id}")
        print(f"  Code: {session.admission_code}")
        print(f"  Status: {session.status}")
        print(f"  is_open: {session.is_open}")
        print(f"  is_close: {session.is_close}")
        print(f"  Opening: {session.opening_date}")
        print(f"  Closing: {session.closing_date}")
        print()

if __name__ == '__main__':
    check_sessions()