import sqlite3

def get_connection():
    return sqlite3.connect("inventory.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER,
        item_name TEXT,
        quantity INTEGER,
        cost_price REAL,
        selling_price REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER,
        item_id INTEGER,
        qty INTEGER,
        total REAL,
        date TEXT DEFAULT CURRENT_DATE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id INTEGER,
        item_id INTEGER,
        qty INTEGER,
        total_cost REAL,
        date TEXT DEFAULT CURRENT_DATE
    )
    """)

    conn.commit()
    conn.close()
