import psycopg2
import streamlit as st

def get_connection():
    return psycopg2.connect(
        st.secrets["DATABASE_URL"],
        sslmode="require"
    )

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE,
        password TEXT,
        name TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id SERIAL PRIMARY KEY,
        vendor_id INT,
        name TEXT,
        quantity INT,
        price NUMERIC
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id SERIAL PRIMARY KEY,
        vendor_id INT,
        item_name TEXT,
        qty INT,
        total NUMERIC,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
