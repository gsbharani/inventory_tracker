import streamlit as st
from db import get_connection

def signup():
    st.subheader("Create Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO vendors (name, email, password) VALUES (%s,%s,%s)",
                (name, email, password)
            )
            conn.commit()
            st.success("Account created. Please login.")
        except:
            st.error("Email already exists")
        cur.close()
        conn.close()

def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name FROM vendors WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            st.session_state.vendor_id = user[0]
            st.session_state.vendor_name = user[1]
            st.rerun()
        else:
            st.error("Invalid credentials")
