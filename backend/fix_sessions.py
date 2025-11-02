#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(__file__))
django.setup()

from portal.models import ApplicationSettings

def fix_existing_sessions():
    sessions = ApplicationSettings.objects.all()
    print(f"Found {sessions.count()} admission sessions")
    print("-" * 60)

    for session in sessions:
        print(f"Processing session ID: {session.id} ({session.admission_code})")

        # Check if the new fields exist and set defaults if needed
        try:
            # Try to access the fields
            is_open = getattr(session, 'is_open', None)
            is_close = getattr(session, 'is_close', None)

            print(f"  Current: is_open={is_open}, is_close={is_close}")

            # Set defaults for existing records
            if is_open is None:
                session.is_open = False
            if is_close is None:
                session.is_close = True

            # Save to update the record
            session.save()
            print(f"  Updated: is_open={session.is_open}, is_close={session.is_close}")

        except AttributeError as e:
            print(f"  Error accessing fields: {e}")
            # Try raw SQL update
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE portal_applicationsettings
                    SET is_open = %s, is_close = %s
                    WHERE id = %s
                """, [False, True, session.id])
                print(f"  Updated via raw SQL")

        print()

    print("All sessions processed!")

if __name__ == '__main__':
    fix_existing_sessions()