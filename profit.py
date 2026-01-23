import streamlit as st
from db import get_connection

def profit_page():
    st.header("Profit")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COALESCE(SUM(total_amount),0) FROM sales WHERE vendor_id=%s",
        (st.session_state.vendor_id,)
    )
    total = cur.fetchone()[0]
    cur.close()
    conn.close()

    st.metric("Total Revenue", f"₹ {total}")
