import streamlit as st
import pandas as pd
import io
from db import get_connection

def items_page():
    st.header("Items")

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT item_id, item_name, category, quantity, selling_price
        FROM items WHERE vendor_id=%s
        """,
        conn,
        params=(st.session_state.vendor_id,)
    )

    st.dataframe(df)

    low_stock = df[df["quantity"] <= 5]
    if not low_stock.empty:
        st.warning("⚠️ Low Stock Items")
        st.dataframe(low_stock)

    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button(
        "⬇️ Export Items",
        data=buffer,
        file_name="items.xlsx"
    )

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
        st.success("Item added")
        st.rerun()

    st.subheader("Import from Excel")
    file = st.file_uploader("Upload Excel", type=["xlsx"])

    if file:
        df_upload = pd.read_excel(file)
        cur = conn.cursor()
        for _, r in df_upload.iterrows():
            cur.execute("""
                INSERT INTO items
                (vendor_id, item_name, category, purchase_price, selling_price, quantity)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                st.session_state.vendor_id,
                r["item_name"],
                r["category"],
                r["purchase_price"],
                r["selling_price"],
                r["quantity"]
            ))
        conn.commit()
        st.success("Imported successfully")

    conn.close()
