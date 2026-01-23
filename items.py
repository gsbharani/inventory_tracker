import streamlit as st
import pandas as pd
import io
from db import get_connection

def items_page():
    st.header("📦 Items")

    conn = get_connection()

    df = pd.read_sql("""
        SELECT item_id, item_name, category, quantity, selling_price
        FROM items
        WHERE vendor_id=%s
    """, conn, params=(st.session_state.vendor_id,))

    st.dataframe(df)

    low = df[df["quantity"] <= 5]
    if not low.empty:
        st.warning("⚠️ Low Stock Alert")
        st.dataframe(low)

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button("⬇️ Export Items", buffer, "items.xlsx")

    st.subheader("Add Item")

    name = st.text_input("Item Name")
    category = st.text_input("Category")
    purchase = st.number_input("Purchase Price")
    selling = st.number_input("Selling Price")
    qty = st.number_input("Quantity", step=1)

    if st.button("Add Item"):
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO items
            (vendor_id, item_name, category, purchase_price, selling_price, quantity)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (st.session_state.vendor_id, name, category, purchase, selling, qty))
        conn.commit()
        st.rerun()

    conn.close()
