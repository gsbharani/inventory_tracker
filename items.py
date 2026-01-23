import streamlit as st
from db import get_connection
import pandas as pd

def items_page():
    st.header("Items")

    name = st.text_input("Item Name")
    category = st.text_input("Category")
    purchase_price = st.number_input("Purchase Price", 0.0)
    selling_price = st.number_input("Selling Price", 0.0)
    qty = st.number_input("Quantity", 0)

    if st.button("Add Item"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO items 
            (vendor_id, item_name, category, purchase_price, selling_price, quantity)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                st.session_state.vendor_id,
                name,
                category,
                purchase_price,
                selling_price,
                qty
            )
        )
        conn.commit()
        cur.close()
        conn.close()
        st.success("Item added")

    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT item_name, category, quantity, purchase_price, selling_price
        FROM items
        WHERE vendor_id = %s
        """,
        conn,
        params=(st.session_state.vendor_id,)
    )
    conn.close()

    st.dataframe(df)
