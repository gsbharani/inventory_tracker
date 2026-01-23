import streamlit as st
from db import get_connection

def dashboard_page():
    st.header("Dashboard")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM items WHERE vendor_id=%s", (st.session_state.vendor_id,))
    items = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(quantity),0) FROM items WHERE vendor_id=%s", (st.session_state.vendor_id,))
    stock = cur.fetchone()[0]

    cur.execute("SELECT COALESCE(SUM(total_amount),0) FROM sales WHERE vendor_id=%s", (st.session_state.vendor_id,))
    sales = cur.fetchone()[0]

    cur.execute("""
        SELECT COALESCE(SUM((i.selling_price - i.purchase_price) * s.quantity),0)
        FROM sales s
        JOIN items i ON s.item_id=i.item_id
        WHERE s.vendor_id=%s
    """, (st.session_state.vendor_id,))
    profit = cur.fetchone()[0]

    conn.close()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Items", items)
    c2.metric("Stock Qty", stock)
    c3.metric("Sales", f"₹ {sales}")
    c4.metric("Profit", f"₹ {profit}")
