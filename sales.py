import streamlit as st
import pandas as pd
from db import get_connection

def sales_page():
    st.header("Sales")

    conn = get_connection()

    df = pd.read_sql(
        "SELECT item_id, item_name, selling_price, quantity FROM items WHERE vendor_id=%s",
        conn,
        params=(st.session_state.vendor_id,)
    )

    item = st.selectbox(
        "Item",
        df.itertuples(index=False),
        format_func=lambda x: f"{x.item_name} (Stock: {x.quantity})"
    )

    qty = st.number_input("Quantity", min_value=1, max_value=int(item.quantity))
    unit_price = st.number_input("Selling Price", value=float(item.selling_price))

    total = qty * unit_price

    if st.button("Record Sale"):
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO sales
            (vendor_id, item_id, quantity, unit_price, total_amount)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                st.session_state.vendor_id,
                int(item.item_id),
                int(qty),
                float(unit_price),
                float(total)
            )
        )

        cur.execute(
            """
            UPDATE items
            SET quantity = quantity - %s,
                selling_price = %s
            WHERE item_id = %s
            """,
            (qty, unit_price, item.item_id)
        )

        conn.commit()
        st.success("Sale recorded")

    st.subheader("Sales History")
    sales_df = pd.read_sql(
        """
        SELECT s.sale_id, i.item_name, s.quantity, s.unit_price, s.total_amount, s.created_at
        FROM sales s
        JOIN items i ON s.item_id=i.item_id
        WHERE s.vendor_id=%s
        ORDER BY s.created_at DESC
        """,
        conn,
        params=(st.session_state.vendor_id,)
    )
    st.dataframe(sales_df)

    conn.close()
