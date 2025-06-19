import sqlite3
import hashlib

def hash_password(password):
    # Hash the password if it's numeric
    if password.isdigit():
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password  # Leave as-is if not numeric

# database setup
def setup_database():
    conn = sqlite3.connect('ProductRegistration.db') 
    cursor = conn.cursor()

    try:
        # Check if 'products' table exists and has unwanted 'barcode' column
        cursor.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'products' in [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")]:
            if 'barcode_data' not in columns or 'barcode_path' not in columns or 'barcode' in columns:
                print("Altering 'products' table schema...")

                # Recreate the table with updated schema
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        batch_id TEXT UNIQUE,
                        product_name TEXT NOT NULL,
                        description TEXT,
                        submission_date TEXT DEFAULT CURRENT_TIMESTAMP,
                        testing_date TEXT NOT NULL,
                        maturity_date TEXT NOT NULL,
                        test_completed TEXT DEFAULT 'No',
                        test_id TEXT,
                        test_result_location TEXT,
                        date_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                        updated_by TEXT,
                        owner_id INTEGER,
                        status TEXT DEFAULT 'Pending',
                        barcode_data TEXT,
                        barcode_path TEXT,
                        FOREIGN KEY (owner_id) REFERENCES product_owners(owner_id)
                    )
                ''')

                # Copy data from old to new (ignore missing new columns for now)
                common_cols = [
                    "id", "batch_id", "product_name", "description", "submission_date",
                    "testing_date", "maturity_date", "test_completed", "test_id",
                    "test_result_location", "date_updated", "updated_by",
                    "owner_id", "status"
                ]
                cursor.execute(f'''
                    INSERT INTO products_new ({", ".join(common_cols)})
                    SELECT {", ".join(common_cols)} FROM products
                ''')

                cursor.execute("DROP TABLE products")
                cursor.execute("ALTER TABLE products_new RENAME TO products")
                print("Schema updated.")
        else:
            # Create products table if it doesn't exist at all
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    batch_id TEXT UNIQUE,
                    product_name TEXT NOT NULL,
                    description TEXT,
                    submission_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    testing_date TEXT NOT NULL,
                    maturity_date TEXT NOT NULL,
                    test_completed TEXT DEFAULT 'No',
                    test_id TEXT,
                    test_result_location TEXT,
                    date_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_by TEXT,
                    owner_id INTEGER,
                    status TEXT DEFAULT 'Pending',
                    barcode_data TEXT,
                    barcode_path TEXT,
                    FOREIGN KEY (owner_id) REFERENCES product_owners(owner_id)
                )
            ''')

        # Create user table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute("SELECT * FROM user WHERE email = 'admin'")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO user (email, password) VALUES (?, ?)", ('admin', 'admin'))
            
        # Create product_owners table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_owners (
                owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                registered_at TEXT
            )
        ''')

        # Create admin table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PO_delete_audit_log (
                log_id INTEGER PRIMARY KEY,
                owner_id INTEGER,
                deleted_by TEXT,
                deleted_at TEXT,
                FOREIGN KEY(owner_id) REFERENCES product_owners(owner_id)
            )
        """)

        conn.commit()

    except sqlite3.Error as e:
        print(f"Error creating or modifying tables: {e}")
        
    finally:
        cursor.close()
        conn.close()

# Admin registration helper
def add_admin(username, password):
    hashed_pw = hash_password(password)

    conn = sqlite3.connect('ProductRegistration.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO admin (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        print(f"Admin '{username}' added.")
    except sqlite3.IntegrityError:
        print(f"Admin '{username}' already exists.")
    finally:
        conn.close()

# Setup
setup_database()
add_admin("admin123", "0000")
