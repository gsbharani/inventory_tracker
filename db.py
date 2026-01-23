import psycopg2
import streamlit as st

def get_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=st.secrets["DB_PORT"],
        sslmode="require"
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        vendor_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        item_id SERIAL PRIMARY KEY,
        vendor_id INT REFERENCES vendors(vendor_id),
        item_name TEXT NOT NULL,
        category TEXT,
        quantity INT DEFAULT 0,
        price FLOAT DEFAULT 0
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sale_id SERIAL PRIMARY KEY,
        vendor_id INT REFERENCES vendors(vendor_id),
        item_id INT REFERENCES items(item_id),
        quantity INT NOT NULL,
        total_price FLOAT NOT NULL,
        sale_date TIMESTAMP DEFAULT NOW()
    );
    """)
    conn.commit()
    conn.close()
