import streamlit as st
from db import get_connection
import pandas as pd

def items_page():
    st.header("Items")

    name = st.text_input("Item Name")
    qty = st.number_input("Quantity", 0)
    price = st.number_input("Price", 0.0)

    if st.button("Add Item"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO items (vendor_id, name, quantity, price) VALUES (%s,%s,%s,%s)",
            (st.session_state.vendor_id, name, qty, price)
        )
        conn.commit()
        cur.close()
        conn.close()
        st.success("Item added")

    conn = get_connection()
    df = pd.read_sql(
        "SELECT name, quantity, price FROM items WHERE vendor_id=%s",
        conn,
        params=(st.session_state.vendor_id,)
    )
    conn.close()
    st.dataframe(df)
