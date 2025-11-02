"""
Check the actual structure of lsc_admins table
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DESCRIBE lsc_admins")
    columns = cursor.fetchall()
    
    print("\n" + "=" * 60)
    print("lsc_admins Table Structure:")
    print("=" * 60)
    for col in columns:
        print(f"  {col[0]:20} {col[1]:20} {col[2]:10} {col[3]:10}")
    print("=" * 60 + "\n")
    
    # Show sample data
    cursor.execute("SELECT * FROM lsc_admins LIMIT 5")
    rows = cursor.fetchall()
    
    if rows:
        print("Sample Data:")
        print("=" * 60)
        for row in rows:
            print(row)
        print("=" * 60 + "\n")
