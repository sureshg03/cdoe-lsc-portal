#!/usr/bin/env python
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from portal.models import ApplicationSettings, SystemSettings
from django.utils import timezone
import datetime

def create_initial_settings():
    print("Creating initial application settings...")

    # Create application settings
    cde_settings, created = ApplicationSettings.objects.get_or_create(
        application_type='CDE',
        defaults={
            'is_open': True,
            'opening_date': timezone.now(),
            'closing_date': timezone.now() + datetime.timedelta(days=30),
            'max_applications': 1000,
            'description': 'CDE Application for Distance Education',
            'instructions': 'Please fill all required fields carefully.'
        }
    )
    if created:
        print("✓ Created CDE application settings")
    else:
        print("✓ CDE application settings already exist")

    deb_settings, created = ApplicationSettings.objects.get_or_create(
        application_type='DEB',
        defaults={
            'is_open': False,
            'max_applications': 500,
            'description': 'DEB Application for Bachelor Degree',
            'instructions': 'DEB applications are currently closed.'
        }
    )
    if created:
        print("✓ Created DEB application settings")
    else:
        print("✓ DEB application settings already exist")

    abc_settings, created = ApplicationSettings.objects.get_or_create(
        application_type='ABC',
        defaults={
            'is_open': False,
            'max_applications': 200,
            'description': 'ABC Application for Advanced Courses',
            'instructions': 'ABC applications are currently closed.'
        }
    )
    if created:
        print("✓ Created ABC application settings")
    else:
        print("✓ ABC application settings already exist")

    print("\nCreating initial system settings...")

    # Create system settings
    settings_data = [
        ('GENERAL', 'site_title', 'Periyar University LSC Portal', 'Main site title'),
        ('GENERAL', 'contact_email', 'admin@periyaruniversity.ac.in', 'Contact email address'),
        ('GENERAL', 'support_phone', '+91-1234567890', 'Support phone number'),
        ('NOTIFICATION', 'email_enabled', 'true', 'Enable email notifications'),
        ('NOTIFICATION', 'sms_enabled', 'false', 'Enable SMS notifications'),
        ('SECURITY', 'session_timeout', '3600', 'Session timeout in seconds'),
        ('SECURITY', 'max_login_attempts', '5', 'Maximum login attempts before lockout'),
        ('MAINTENANCE', 'maintenance_mode', 'false', 'Enable maintenance mode'),
    ]

    for setting_type, key, value, description in settings_data:
        setting, created = SystemSettings.objects.get_or_create(
            setting_type=setting_type,
            key=key,
            defaults={
                'value': value,
                'description': description,
                'is_active': True
            }
        )
        if created:
            print(f"✓ Created {setting_type}: {key}")
        else:
            print(f"✓ {setting_type}: {key} already exists")

    print("\n✅ Initial settings data created successfully!")

if __name__ == '__main__':
    create_initial_settings()