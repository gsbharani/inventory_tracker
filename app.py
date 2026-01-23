import streamlit as st
from auth import login, signup
from dashboard import dashboard_page
from items import items_page
from sales import sales_page
from profit import profit_page
from analytics import analytics_page

st.set_page_config("Inventory SaaS", layout="wide")

if "vendor_id" not in st.session_state:
    choice = st.radio("Choose", ["Login", "Sign Up"])
    if choice == "Login":
        login()
    else:
        signup()
else:
    st.sidebar.success(f"Welcome {st.session_state.vendor_name}")

    page = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Items", "Sales", "Analytics", "Profit"]
    )

    if page == "Dashboard":
        dashboard_page()
    elif page == "Items":
        items_page()
    elif page == "Sales":
        sales_page()
    elif page == "Analytics":
        analytics_page()
    elif page == "Profit":
        profit_page()
