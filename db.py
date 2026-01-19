import sqlite3

def get_connection():
    return sqlite3.connect("inventory.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        category TEXT,
        quantity INTEGER,
        cost_price REAL,
        selling_price REAL,
        min_stock INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        qty INTEGER,
        selling_price REAL,
        total REAL,
        customer TEXT,
        sale_date DATE DEFAULT CURRENT_DATE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        qty INTEGER,
        cost_price REAL,
        total REAL,
        vendor TEXT,
        purchase_date DATE DEFAULT CURRENT_DATE
    )
    """)

    conn.commit()
    conn.close()
