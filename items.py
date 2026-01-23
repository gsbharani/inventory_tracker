import streamlit as st
import pandas as pd
from db import get_connection
from datetime import datetime

def items_page():
    st.title("Items Management")
    conn = get_connection()
    cur = conn.cursor()

    # ---------------- Add New Item ----------------
    with st.expander("Add New Item"):
        item_name = st.text_input("Item Name")
        category = st.text_input("Category")
        purchase_price = st.number_input("Purchase Price", min_value=0.0)
        selling_price = st.number_input("Selling Price", min_value=0.0)
        quantity = st.number_input("Quantity", min_value=0)

        if st.button("Add Item"):
            cur.execute(
                """
                INSERT INTO items (vendor_id, item_name, category, purchase_price, selling_price, quantity, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """,
                (
                    st.session_state.vendor_id,
                    item_name,
                    category,
                    purchase_price,
                    selling_price,
                    quantity
                )
            )
            conn.commit()
            st.success(f"Item '{item_name}' added successfully!")

    st.markdown("---")

    # ---------------- Bulk Import ----------------
    st.subheader("Bulk Import Items from Excel/CSV")
    uploaded_file = st.file_uploader("Upload Excel or CSV", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.write("Preview of uploaded data")
            st.dataframe(df.head())

            if st.button("Import Items"):
                for _, row in df.iterrows():
                    cur.execute(
                        """
                        INSERT INTO items (vendor_id, item_name, category, purchase_price, selling_price, quantity, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW())
                        """,
                        (
                            st.session_state.vendor_id,
                            row["item_name"],
                            row["category"],
                            row["purchase_price"],
                            row["selling_price"],
                            row["quantity"]
                        )
                    )
                conn.commit()
                st.success("Items imported successfully!")

        except Exception as e:
            st.error(f"Error importing file: {e}")

    st.markdown("---")

    # ---------------- Show Items Table ----------------
    st.subheader("Your Items")
    try:
        df_items = pd.read_sql(
            "SELECT item_id, item_name, category, purchase_price, selling_price, quantity FROM items WHERE vendor_id=%s",
            conn,
            params=(st.session_state.vendor_id,)
        )
        st.dataframe(df_items)

        # ---------------- Low Stock Alert ----------------
        low_stock = df_items[df_items["quantity"] < 10]
        if not low_stock.empty:
            st.warning("Low Stock Items:")
            st.dataframe(low_stock[["item_name", "quantity"]])

        # ---------------- Edit / Delete ----------------
        selected_item = st.selectbox("Select Item to Edit/Delete", df_items["item_name"])
        if selected_item:
            item_row = df_items[df_items["item_name"] == selected_item].iloc[0]

            new_name = st.text_input("Item Name", value=item_row["item_name"])
            new_category = st.text_input("Category", value=item_row["category"])
            new_purchase = st.number_input("Purchase Price", value=float(item_row["purchase_price"]))
            new_selling = st.number_input("Selling Price", value=float(item_row["selling_price"]))
            new_quantity = st.number_input("Quantity", value=int(item_row["quantity"]))

            if st.button("Update Item"):
                cur.execute(
                    """
                    UPDATE items
                    SET item_name=%s, category=%s, purchase_price=%s, selling_price=%s, quantity=%s
                    WHERE item_id=%s AND vendor_id=%s
                    """,
                    (new_name, new_category, new_purchase, new_selling, new_quantity, item_row["item_id"], st.session_state.vendor_id)
                )
                conn.commit()
                st.success("Item updated successfully!")
                st.experimental_rerun()

            if st.button("Delete Item"):
                cur.execute(
                    "DELETE FROM items WHERE item_id=%s AND vendor_id=%s",
                    (item_row["item_id"], st.session_state.vendor_id)
                )
                conn.commit()
                st.success("Item deleted successfully!")
                st.experimental_rerun()

        # ---------------- Export to Excel ----------------
        if st.button("Export Items to Excel"):
            df_items.to_excel("my_items.xlsx", index=False)
            with open("my_items.xlsx", "rb") as f:
                st.download_button("Download Excel", f, file_name="my_items.xlsx")

    except Exception as e:
        st.error(f"Error loading items: {e}")
