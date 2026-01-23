from db import get_connection
import streamlit as st

def profit_page():
    vid = st.session_state.vendor_id
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            SUM((selling_price - purchase_price) * quantity)
        FROM items
        WHERE vendor_id=%s
    """, (vid,))

    profit = cur.fetchone()[0] or 0
    st.metric("Total Profit", f"₹ {profit}")
