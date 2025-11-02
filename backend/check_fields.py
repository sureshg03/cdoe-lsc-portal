#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(__file__))
django.setup()

from portal.models import ApplicationSettings

def check_model_fields():
    print("Model fields:")
    for field in ApplicationSettings._meta.fields:
        print(f"  - {field.name}: {field.__class__.__name__}")

    print("\nChecking first session:")
    session = ApplicationSettings.objects.first()
    if session:
        print(f"ID: {session.id}")
        print(f"is_open: {getattr(session, 'is_open', 'NOT FOUND')}")
        print(f"is_close: {getattr(session, 'is_close', 'NOT FOUND')}")
        print(f"status: {session.status}")
    else:
        print("No sessions found")

if __name__ == '__main__':
    check_model_fields()