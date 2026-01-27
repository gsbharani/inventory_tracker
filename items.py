import streamlit as st
import pandas as pd
from db import get_connection
from datetime import datetime

def items_page():
    st.title("Items Management")
    conn = get_connection()
    cur = conn.cursor()

    # ----------------- Add / Edit Items -----------------
    with st.expander("Add / Update Item"):
        item_name = st.text_input("Item Name")
        category = st.text_input("Category")
        purchase_price = st.number_input("Purchase Price", min_value=0.0, step=0.01)
       
        quantity = st.number_input("Quantity", min_value=0, step=1)

        if st.button("Add / Update Item"):
            cur.execute(
                """
                INSERT INTO items (vendor_id, item_name, category, purchase_price,  quantity, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (vendor_id, item_name) DO UPDATE 
                SET category=EXCLUDED.category,
                    purchase_price=EXCLUDED.purchase_price,
                   
                    quantity=EXCLUDED.quantity,
                    created_at=EXCLUDED.created_at
                """,
                (st.session_state.vendor_id, item_name, category, purchase_price,  quantity, datetime.now())
            )
            conn.commit()
            st.success(f"Item '{item_name}' added/updated successfully!")

    # ----------------- Bulk Upload via Excel -----------------
    st.subheader("Bulk Upload Items")
    uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        expected_cols = {"item_name", "category", "purchase_price",  "quantity"}
        if not expected_cols.issubset(df.columns):
            st.error(f"Excel must have columns: {expected_cols}")
        else:
            for _, row in df.iterrows():
                cur.execute(
                    """
                    INSERT INTO items (vendor_id, item_name, category, purchase_price,  quantity, created_at)
                    VALUES (%s, %s, %s, %s,  %s, %s)
                    ON CONFLICT (vendor_id, item_name) DO UPDATE 
                    SET category=EXCLUDED.category,
                        purchase_price=EXCLUDED.purchase_price,
                       
                        quantity=EXCLUDED.quantity,
                        created_at=EXCLUDED.created_at
                    """,
                    (
                        st.session_state.vendor_id,
                        row["item_name"],
                        row["category"],
                        row["purchase_price"],
                        
                        row["quantity"],
                        datetime.now()
                    )
                )
            conn.commit()
            st.success("Bulk upload completed!")

    # ----------------- Display Items -----------------
    df_items = pd.read_sql(
        "SELECT item_name, category, purchase_price,  quantity FROM items WHERE vendor_id=%s",
        conn,
        params=(st.session_state.vendor_id,)
    )
    st.dataframe(df_items)

    # ----------------- Low Stock Alert -----------------
    st.subheader("Low Stock Items")
    low_stock_threshold = st.number_input("Low Stock Threshold", value=5, min_value=1, step=1)
    low_stock_items = df_items[df_items["quantity"] <= low_stock_threshold]
    if not low_stock_items.empty:
        st.warning(f"Low stock alert for {len(low_stock_items)} item(s)!")
        st.dataframe(low_stock_items)
    else:
        st.success("No low stock items.")

    # ----------------- Export Items -----------------
    if st.button("Export Items to Excel"):
        df_items.to_excel("items_export.xlsx", index=False)
        with open("items_export.xlsx", "rb") as f:
            st.download_button("Download Excel", f, file_name="items_export.xlsx")
