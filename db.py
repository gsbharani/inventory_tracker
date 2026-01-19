import sqlite3

DB_NAME = "inventory.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT,
        quantity INTEGER DEFAULT 0,
        cost_price REAL DEFAULT 0,
        selling_price REAL DEFAULT 0,
        min_stock INTEGER DEFAULT 0
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
        sale_date TEXT DEFAULT CURRENT_DATE
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
        purchase_date TEXT DEFAULT CURRENT_DATE
    )
    """)

    conn.commit()
    conn.close()
