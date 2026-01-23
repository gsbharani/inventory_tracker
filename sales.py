import streamlit as st
import pandas as pd
from db import get_connection
from datetime import datetime

def sales_page():
    st.title("Sales Management")
    conn = get_connection()
    cur = conn.cursor()

    # ---------------- Add Sale ----------------
    st.subheader("Record a Sale")
    try:
        # Fetch items for the vendor
        items_df = pd.read_sql(
            "SELECT item_id, item_name, quantity, selling_price FROM items WHERE vendor_id=%s",
            conn,
            params=(st.session_state.vendor_id,)
        )
        if items_df.empty:
            st.info("No items found. Please add items first.")
            return

        selected_item = st.selectbox("Select Item", items_df["item_name"])
        item_row = items_df[items_df["item_name"] == selected_item].iloc[0]

        max_qty = int(item_row["quantity"])
        qty = st.number_input("Quantity Sold", min_value=1, max_value=max_qty, value=1)

        if st.button("Record Sale"):
            total_amount = qty * float(item_row["selling_price"])

            # Insert into sales table
            cur.execute(
                """
                INSERT INTO sales (vendor_id, item_id, quantity, total_amount, created_at)
                VALUES (%s, %s, %s, %s, NOW())
                """,
                (st.session_state.vendor_id, item_row["item_id"], qty, total_amount)
            )

            # Deduct stock from items
            cur.execute(
                "UPDATE items SET quantity = quantity - %s WHERE item_id=%s AND vendor_id=%s",
                (qty, item_row["item_id"], st.session_state.vendor_id)
            )

            conn.commit()
            st.success(f"Sale recorded! Total: ₹{total_amount:.2f}")
            st.experimental_rerun()

    except Exception as e:
        st.error(f"Error recording sale: {e}")

    st.markdown("---")

    # ---------------- Sales Report ----------------
    st.subheader("Sales Report")
    try:
        sales_df = pd.read_sql(
            """
            SELECT s.sale_id, i.item_name, s.quantity, s.total_amount, s.created_at
            FROM sales s
            JOIN items i ON s.item_id = i.item_id
            WHERE s.vendor_id=%s
            ORDER BY s.created_at DESC
            """,
            conn,
            params=(st.session_state.vendor_id,)
        )

        if not sales_df.empty:
            st.dataframe(sales_df)

            # Export report
            if st.button("Export Sales to Excel"):
                sales_df.to_excel("sales_report.xlsx", index=False)
                with open("sales_report.xlsx", "rb") as f:
                    st.download_button("Download Excel", f, file_name="sales_report.xlsx")

            # ---------------- Sales Analytics ----------------
            st.subheader("Sales Analytics")
            sales_summary = sales_df.groupby("item_name")["total_amount"].sum().reset_index()
            sales_summary = sales_summary.sort_values("total_amount", ascending=False)
            st.bar_chart(data=sales_summary, x="item_name", y="total_amount")
        else:
            st.info("No sales recorded yet.")

    except Exception as e:
        st.error(f"Error loading sales report: {e}")
