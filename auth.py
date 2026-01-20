import streamlit as st
from db import get_connection

def signup():
    st.subheader("Vendor Signup")
    business = st.text_input("Business Name", key="signup_business")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    

    if st.button("Create Account"):
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO vendors (business_name, email, password) VALUES (?,?,?)",
                (business, email, password)
            )
            conn.commit()
            st.success("Account created. Please login.")
        except:
            st.error("Email already exists")
        conn.close()

def login():
    st.subheader("Vendor Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
   

    if st.button("Login"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT vendor_id, business_name FROM vendors WHERE email=? AND password=?",
            (email, password)
        )
        vendor = cur.fetchone()
        conn.close()

        if vendor:
            st.session_state.logged_in = True
            st.session_state.vendor_id = vendor[0]
            st.session_state.business = vendor[1]
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")
