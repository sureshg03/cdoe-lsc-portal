"""
Script to remove portal_applicationsettings table from old database locations
"""
import MySQLdb
import sys

def drop_table_from_database(db_name):
    """Drop portal_applicationsettings from specified database"""
    try:
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            port=3306,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'portal_applicationsettings'")
        if cursor.fetchone():
            # Table exists, drop it
            cursor.execute("DROP TABLE portal_applicationsettings")
            print(f"✓ Dropped portal_applicationsettings from {db_name}")
            conn.commit()
        else:
            print(f"  - No portal_applicationsettings table found in {db_name}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error dropping table from {db_name}: {e}")
        return False

def main():
    print("=" * 60)
    print("Cleanup Old Portal Tables")
    print("=" * 60)
    print("\nThis will remove portal_applicationsettings from:")
    print("  - lsc_portal_db")
    print("  - online_edu")
    print("\nThe table will remain in lsc_admindb (correct location)")
    
    # Ask for confirmation
    response = input("\nProceed with cleanup? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("\nCleanup cancelled.")
        sys.exit(0)
    
    print("\nStarting cleanup...\n")
    
    # Drop from lsc_portal_db
    drop_table_from_database('lsc_portal_db')
    
    # Drop from online_edu
    drop_table_from_database('online_edu')
    
    print("\n" + "=" * 60)
    print("✓ Cleanup completed!")
    print("=" * 60)
    print("\nPortal tables are now only in lsc_admindb")

if __name__ == '__main__':
    main()
