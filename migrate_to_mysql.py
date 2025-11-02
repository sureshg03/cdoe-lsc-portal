#!/usr/bin/env python
"""
Script to migrate data from SQLite to MySQL using Django fixtures
"""
import os
import sys
import django
import json
from django.core import serializers
from django.conf import settings

def main():
    # Add backend directory to Python path
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

    # Setup Django with SQLite
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

    print("📤 Dumping data from SQLite...")

    # Get all model classes
    from django.apps import apps
    models = apps.get_models()

    # Serialize all data
    data = []
    for model in models:
        if model._meta.app_label in ['lsc_auth', 'portal', 'auth', 'contenttypes', 'sessions']:
            print(f"  Dumping {model._meta.label}...")
            objects = model.objects.all()
            data.extend(serializers.serialize('json', objects))

    # Save to fixture file
    with open('data_dump.json', 'w') as f:
        f.write(json.dumps(data, indent=2))

    print("✅ Data dumped to data_dump.json")

    # Now switch to MySQL and load the data
    print("🔄 Switching to MySQL database...")

    # Use subprocess to run loaddata with MySQL settings
    import subprocess
    import sys

    result = subprocess.run([
        sys.executable, 'manage.py', 'loaddata', '../data_dump.json'
    ], cwd=os.path.join(os.path.dirname(__file__), 'backend'), capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Migration completed!")
        print(result.stdout)
    else:
        print("❌ Migration failed!")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

if __name__ == '__main__':
    main()