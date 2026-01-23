import streamlit as st
from db import get_connection

def sales_page():
    st.header("Sales")

    item_id = st.number_input("Item ID", step=1)
    qty = st.number_input("Quantity", step=1, min_value=1)

    if st.button("Record Sale"):
        conn = get_connection()
        cur = conn.cursor()

        # Get selling price
        cur.execute(
            "SELECT selling_price, quantity FROM items WHERE item_id=%s AND vendor_id=%s",
            (item_id, st.session_state.vendor_id)
        )
        row = cur.fetchone()

        if not row:
            st.error("Invalid item")
            return

        price, stock = row

        if qty > stock:
            st.error("Not enough stock")
            return

        total = price * qty

        # TRANSACTION
        cur.execute(
            "INSERT INTO sales (vendor_id, item_id, quantity, total_amount) VALUES (%s,%s,%s,%s)",
            (st.session_state.vendor_id, item_id, qty, total)
        )

        cur.execute(
            "UPDATE items SET quantity = quantity - %s WHERE item_id=%s",
            (qty, item_id)
        )

        conn.commit()
        conn.close()

        st.success("Sale recorded & stock updated")
