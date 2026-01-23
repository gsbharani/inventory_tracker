import streamlit as st
from db import get_connection
import pandas as pd

def sales_page():
    st.header("Sales")

    item = st.text_input("Item Name")
    qty = st.number_input("Qty Sold", 1)
    total = st.number_input("Total Amount", 0.0)

    if st.button("Add Sale"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sales (vendor_id, item_name, qty, total) VALUES (%s,%s,%s,%s)",
            (st.session_state.vendor_id, item, qty, total)
        )
        conn.commit()
        cur.close()
        conn.close()
        st.success("Sale added")

    conn = get_connection()
    df = pd.read_sql(
        "SELECT item_name, qty, total, created_at FROM sales WHERE vendor_id=%s",
        conn,
        params=(st.session_state.vendor_id,)
    )
    conn.close()
    st.dataframe(df)
