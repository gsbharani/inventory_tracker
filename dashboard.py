import streamlit as st
from db import get_connection

def dashboard():
    st.title(f"Welcome {st.session_state.business}")

    conn = get_connection()

    st.subheader("Add Item")
    name = st.text_input("Item Name")
    qty = st.number_input("Quantity", 1)
    cp = st.number_input("Cost Price")
    sp = st.number_input("Selling Price")

    if st.button("Save Item"):
        conn.execute("""
        INSERT INTO items (vendor_id, item_name, quantity, cost_price, selling_price)
        VALUES (?,?,?,?,?)
        """, (st.session_state.vendor_id, name, qty, cp, sp))
        conn.commit()
        st.success("Item added")

    st.subheader("Add Sale")
    item_id = st.number_input("Item ID")
    sale_qty = st.number_input("Sale Qty", 1)

    if st.button("Add Sale"):
        cur = conn.cursor()
        cur.execute(
            "SELECT selling_price FROM items WHERE item_id=? AND vendor_id=?",
            (item_id, st.session_state.vendor_id)
        )
        price = cur.fetchone()[0]
        total = price * sale_qty

        conn.execute("""
        INSERT INTO sales (vendor_id, item_id, qty, total)
        VALUES (?,?,?,?)
        """, (st.session_state.vendor_id, item_id, sale_qty, total))
        conn.commit()
        st.success("Sale added")

    conn.close()
