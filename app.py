import streamlit as st
from auth import login
from items import items_page
from sales import sales_page
from profit import profit_page

st.set_page_config("Inventory SaaS", layout="wide")

if "vendor_id" not in st.session_state:
    st.title("Vendor Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(email, password)
        if user:
            st.session_state.vendor_id = user[0]
            st.session_state.vendor_name = user[1]
            st.rerun()
        else:
            st.error("Invalid login")
else:
    st.sidebar.success(f"Welcome {st.session_state.vendor_name}")
    page = st.sidebar.selectbox("Menu", ["Items", "Sales", "Profit"])

    if page == "Items":
        items_page()
    elif page == "Sales":
        sales_page()
    elif page == "Profit":
        profit_page()
