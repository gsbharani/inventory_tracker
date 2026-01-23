from db import get_connection
import streamlit as st

def items_page():
    vid = st.session_state.vendor_id
    conn = get_connection()
    cur = conn.cursor()

    name = st.text_input("Item name")
    buy = st.number_input("Purchase price")
    sell = st.number_input("Selling price")
    qty = st.number_input("Quantity", step=1)

    if st.button("Add Item"):
        cur.execute("""
            INSERT INTO items (vendor_id, item_name, purchase_price, selling_price, quantity)
            VALUES (%s,%s,%s,%s,%s)
        """, (vid, name, buy, sell, qty))
        conn.commit()
        st.success("Item added")

    cur.execute("SELECT item_name, quantity FROM items WHERE vendor_id=%s", (vid,))
    st.dataframe(cur.fetchall())

