import streamlit as st
from db import get_connection

def signup(name, email, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO vendors (name, email, password) VALUES (%s, %s, %s) RETURNING vendor_id;",
            (name, email, password)
        )
        vendor_id = cur.fetchone()[0]
        conn.commit()
        return vendor_id
    except Exception as e:
        st.error("Email already exists")
        return None
    finally:
        conn.close()

def login(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT vendor_id, name FROM vendors WHERE email=%s AND password=%s;",
        (email, password)
    )
    user = cur.fetchone()
    conn.close()
    return user
