import streamlit as st
from db import get_connection

def profit_page():
    st.header("💰 Profit Summary")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(SUM((i.selling_price - i.purchase_price) * s.quantity),0)
        FROM sales s
        JOIN items i ON s.item_id=i.item_id
        WHERE s.vendor_id=%s
    """, (st.session_state.vendor_id,))

    profit = cur.fetchone()[0]
    conn.close()

    st.metric("Total Profit", f"₹ {profit}")
