import streamlit as st
from db import get_connection

def items_page():
    vendor_id = st.session_state.vendor_id
    st.header("Your Items")

    # Add item
    with st.form("add_item"):
        name = st.text_input("Item Name")
        category = st.text_input("Category")
        quantity = st.number_input("Quantity", 0)
        price = st.number_input("Price", 0.0, step=0.01)
        submitted = st.form_submit_button("Add Item")
        if submitted:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO items (vendor_id, item_name, category, quantity, price) VALUES (%s, %s, %s, %s, %s)",
                (vendor_id, name, category, quantity, price)
            )
            conn.commit()
            conn.close()
            st.success(f"Item {name} added!")

    # Show vendor's items
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT item_id, item_name, category, quantity, price FROM items WHERE vendor_id=%s;", (vendor_id,))
    data = cur.fetchall()
    conn.close()
    st.table(data)
