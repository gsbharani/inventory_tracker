import streamlit as st
from auth import login, signup
from items import items_page
from sales import sales_page
from profit import profit_page
from db import create_tables

st.set_page_config("Inventory SaaS", layout="wide")
create_tables()

if "vendor_id" not in st.session_state:
    choice = st.radio("Choose", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    name = st.text_input("Name") if choice == "Sign Up" else None

    if st.button(choice):
        if choice == "Login":
            user = login(email, password)
            if user:
                st.session_state.vendor_id = user[0]
                st.session_state.vendor_name = user[1]
                st.rerun()
            else:
                st.error("Invalid credentials")
        else:
            vendor_id = signup(name, email, password)
            if vendor_id:
                st.session_state.vendor_id = vendor_id
                st.session_state.vendor_name = name
                st.rerun()
else:
    st.sidebar.success(f"Welcome {st.session_state.vendor_name}")
    page = st.sidebar.selectbox("Menu", ["Items", "Sales", "Profit"])
    if page == "Items":
        items_page()
    elif page == "Sales":
        sales_page()
    elif page == "Profit":
        profit_page()
