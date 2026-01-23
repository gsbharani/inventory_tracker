import streamlit as st
from db import get_connection

def sales_page():
    vendor_id = st.session_state.vendor_id
    st.header("Sales")

    # Record Sale
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT item_id, item_name, quantity, price FROM items WHERE vendor_id=%s;", (vendor_id,))
    items = cur.fetchall()
    conn.close()

    item_dict = {f"{i[1]} (Stock: {i[2]})": i for i in items}

    with st.form("sale_form"):
        selected = st.selectbox("Select Item", list(item_dict.keys()))
        quantity = st.number_input("Quantity Sold", 1, min_value=1)
        submitted = st.form_submit_button("Record Sale")
        if submitted:
            item = item_dict[selected]
            if quantity > item[2]:
                st.error("Not enough stock")
            else:
                total_price = quantity * item[3]
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO sales (vendor_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
                    (vendor_id, item[0], quantity, total_price)
                )
                cur.execute("UPDATE items SET quantity = quantity - %s WHERE item_id=%s", (quantity, item[0]))
                conn.commit()
                conn.close()
                st.success(f"Sale recorded! Total: {total_price}")
