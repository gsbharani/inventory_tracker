import streamlit as st
from db import create_tables
from auth import login, signup
from dashboard import dashboard
from profit_report import profit_report

st.set_page_config("Inventory SaaS", layout="wide")
create_tables()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Signup"])
    with tab1:
        login()
    with tab2:
        signup()
else:
    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Profit Report", "Logout"]
    )

    if menu == "Dashboard":
        dashboard()
    elif menu == "Profit Report":
        profit_report()
    else:
        st.session_state.clear()
        st.experimental_rerun()
