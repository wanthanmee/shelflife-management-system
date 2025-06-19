import sqlite3

def rename_audit_table(new_name="PO_delete_audit_log"):
    try:
        conn = sqlite3.connect("ProductRegistration.db")
        cursor = conn.cursor()
        
        # Check if table exists first
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PO_audit_log'")
        if cursor.fetchone():
            cursor.execute(f"ALTER TABLE PO_audit_log RENAME TO {new_name}")
            conn.commit()
            print(f"Table renamed to '{new_name}' successfully")
        else:
            print("Original table not found")
    except sqlite3.Error as e:
        print(f"Error renaming table: {e}")
    finally:
        if conn:
            conn.close()

# Usage
rename_audit_table("PO_delete_audit_log")  # Or your preferred new name