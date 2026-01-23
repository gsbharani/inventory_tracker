import streamlit as st
from db import get_connection

def signup():
    st.subheader("Create Vendor Account")

    business = st.text_input("Business Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                """
                INSERT INTO vendors (business_name, email, password)
                VALUES (%s, %s, %s)
                """,
                (business, email, password)
            )
            conn.commit()
            st.success("Account created. Please login.")
        except Exception as e:
            st.error("Email already exists")

def login():
    st.subheader("Vendor Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT vendor_id, business_name
            FROM vendors
            WHERE email=%s AND password=%s
            """,
            (email, password)
        )

        vendor = cur.fetchone()

        if vendor:
            st.session_state["vendor_id"] = vendor[0]
            st.session_state["vendor_name"] = vendor[1]
            st.rerun()
        else:
            st.error("Invalid login")
