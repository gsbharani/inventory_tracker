import streamlit as st
from db import get_connection
import pandas as pd

def sales_page():
    st.header("Sales")

    conn = get_connection()
    cur = conn.cursor()

    # Load items for dropdown
    cur.execute(
        "SELECT item_id, item_name, selling_price, quantity FROM items WHERE vendor_id = %s",
        (st.session_state.vendor_id,)
    )
    items = cur.fetchall()

    if not items:
        st.warning("No items available")
        return

    item_map = {
        f"{i[1]} (Stock: {i[3]})": i for i in items
    }

    selected = st.selectbox("Select Item", item_map.keys())
    sell_qty = st.number_input("Quantity to Sell", min_value=1)

    if st.button("Make Sale"):
        item_id, name, price, stock = item_map[selected]

        if sell_qty > stock:
            st.error("Not enough stock")
            return

        total = price * sell_qty

        try:
            cur.execute(
                """
                INSERT INTO sales (vendor_id, item_id, quantity, total_amount)
                VALUES (%s, %s, %s, %s)
                """,
                (st.session_state.vendor_id, item_id, sell_qty, total)
            )

            cur.execute(
                "UPDATE items SET quantity = quantity - %s WHERE item_id = %s",
                (sell_qty, item_id)
            )

            conn.commit()
            st.success(f"Sale completed ₹{total}")

        except Exception as e:
            conn.rollback()
            st.error("Sale failed")

    cur.close()
    conn.close()
