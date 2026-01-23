import streamlit as st
from db import get_connection

def profit_page():
    vendor_id = st.session_state.vendor_id
    st.header("Profit Report")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT SUM(total_price) FROM sales WHERE vendor_id=%s;",
        (vendor_id,)
    )
    profit = cur.fetchone()[0]
    conn.close()
    st.write(f"Total Profit: {profit if profit else 0}")
