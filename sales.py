
import streamlit as st
from db import get_connection

def sales_page():
    st.header("Sales & Purchases")

    conn = get_connection()
    cur = conn.cursor()

    with st.form("add_sale"):
        item_id = st.number_input("Item ID", step=1)
        quantity = st.number_input("Quantity", step=1)
        price = st.number_input("Price", step=0.01)
        submit = st.form_submit_button("Add Sale")

        if submit:
            cur.execute(
                """
                INSERT INTO sales (item_id, quantity, price)
                VALUES (%s, %s, %s)
                """,
                (item_id, quantity, price)
            )
            conn.commit()
            st.success("Sale added")
