import sqlite3
import hashlib



def hash_password(password):
    # Hash the password if it's numeric
    if password.isdigit():
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        return hashed
    return password  # Leave as-is if not numeric

#database setup
def setup_database():
    #create a database connection and cursor
    conn = sqlite3.connect('ProductRegistration.db') 
    cursor = conn.cursor()

    try:
        # Create a table if it doesn't exist
        cursor.execute('''
            CREATE TABLE products (
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
                FOREIGN KEY (owner_id) REFERENCES product_owners(owner_id)
            )
        ''')
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
            
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_owners(
                owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,  -- Enforce uniqueness
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
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        
    finally:
        cursor.close()
        conn.close()

def add_admin(username, password):
    hashed_pw = hash_password(password)

    conn = sqlite3.connect('ProductRegistration.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO admin (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        print(f"User '{username}' added.")
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists.")
    finally:
        conn.close()

setup_database()
add_admin("admin123", "0000")