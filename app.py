import streamlit as st
from db import create_tables
from auth import login, signup
from items import items_page
from sales import sales_page
from profit import profit_page

st.set_page_config("Inventory SaaS", layout="wide")
create_tables()

if "vendor_id" not in st.session_state:
    choice = st.radio("Choose", ["Login", "Sign Up"])
    if choice == "Login":
        login()
    else:
        signup()
else:
    st.sidebar.success(f"Welcome {st.session_state.vendor_name}")
    page = st.sidebar.selectbox("Menu", ["Items", "Sales", "Profit"])

    if page == "Items":
        items_page()
    elif page == "Sales":
        sales_page()
    elif page == "Profit":
        profit_page()
