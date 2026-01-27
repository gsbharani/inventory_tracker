import streamlit as st
import pandas as pd
from db import get_connection
from io import BytesIO


def sales_page():
    st.title("Sales Management")

    conn = get_connection()

    # ---------------- Record Sale ----------------
    st.header("Record Sale")

    df = pd.read_sql(
        """
        SELECT item_id, item_name, selling_price, quantity
        FROM items
        WHERE vendor_id = %s
        """,
        conn,
        params=(int(st.session_state.vendor_id),)
    )

    if df.empty:
        st.info("No items available. Add items before recording sales.")
        return

    item = st.selectbox(
        "Item",
        df.itertuples(index=False),
        format_func=lambda x: f"{x.item_name} (Stock: {x.quantity})"
    )

    qty = st.number_input(
        "Quantity",
        min_value=1,
        max_value=int(item.quantity)
    )

    total = float(qty) * float(item.selling_price)

    if st.button("Save Sale"):
        try:
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO sales (vendor_id, item_id, quantity, total_amount)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    int(st.session_state.vendor_id),
                    int(item.item_id),
                    int(qty),
                    total
                )
            )

            cur.execute(
                """
                UPDATE items
                SET quantity = quantity - %s
                WHERE item_id = %s
                """,
                (int(qty), int(item.item_id))
            )

            conn.commit()
            st.success("Sale recorded successfully ✅")
            st.rerun()

        except Exception as e:
            conn.rollback()
            st.error(f"Error recording sale: {e}")

    st.divider()

    # ---------------- Sales Report ----------------
    st.subheader("Sales Report")

    try:
        sales_df = pd.read_sql(
            """
            SELECT s.sale_id,
                   i.item_name,
                   s.quantity,
                   s.total_amount,
                   s.created_at
            FROM sales s
            JOIN items i ON s.item_id = i.item_id
            WHERE s.vendor_id = %s
            ORDER BY s.created_at DESC
            """,
            conn,
            params=(int(st.session_state.vendor_id),)
        )

        if sales_df.empty:
            st.info("No sales recorded yet.")
            return

        st.dataframe(sales_df, use_container_width=True)

        # ---------------- Export ----------------
        output = BytesIO()
        sales_df.to_excel(output, index=False)
        output.seek(0)

        st.download_button(
            "📥 Download Sales Report (Excel)",
            data=output,
            file_name="sales_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # ---------------- Analytics ----------------
        st.subheader("Sales Analytics")

        summary = (
            sales_df
            .groupby("item_name", as_index=False)["total_amount"]
            .sum()
            .sort_values("total_amount", ascending=False)
        )

        st.bar_chart(summary, x="item_name", y="total_amount")

    except Exception as e:
        st.error(f"Error loading sales report: {e}")
