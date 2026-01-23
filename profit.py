import streamlit as st
import pandas as pd
from db import get_connection

def profit_page():
    st.title("Profit Analytics")
    conn = get_connection()
    cur = conn.cursor()

    try:
        # ---------------- Fetch sales with purchase & selling prices ----------------
        profit_df = pd.read_sql(
            """
            SELECT 
                s.sale_id,
                i.item_name,
                s.quantity,
                i.purchase_price,
                i.selling_price,
                s.total_amount,
                s.created_at
            FROM sales s
            JOIN items i ON s.item_id = i.item_id
            WHERE s.vendor_id=%s
            ORDER BY s.created_at DESC
            """,
            conn,
            params=(st.session_state.vendor_id,)
        )

        if profit_df.empty:
            st.info("No sales recorded yet.")
            return

        # ---------------- Calculate profit ----------------
        profit_df["profit_per_item"] = (profit_df["selling_price"] - profit_df["purchase_price"]) * profit_df["quantity"]
        total_profit = profit_df["profit_per_item"].sum()
        st.metric("Total Profit", f"₹{total_profit:.2f}")

        # ---------------- Profit per item ----------------
        st.subheader("Profit by Item")
        item_profit = profit_df.groupby("item_name")["profit_per_item"].sum().reset_index()
        item_profit = item_profit.sort_values("profit_per_item", ascending=False)
        st.dataframe(item_profit)
        st.bar_chart(data=item_profit, x="item_name", y="profit_per_item")

        # ---------------- Profit over time ----------------
        st.subheader("Profit Over Time")
        profit_time = profit_df.groupby(profit_df["created_at"].dt.date)["profit_per_item"].sum().reset_index()
        st.line_chart(data=profit_time.rename(columns={"created_at": "Date", "profit_per_item": "Profit"}), x="Date", y="Profit")

        # ---------------- Export Profit Report ----------------
        if st.button("Export Profit Report to Excel"):
            profit_df.to_excel("profit_report.xlsx", index=False)
            with open("profit_report.xlsx", "rb") as f:
                st.download_button("Download Excel", f, file_name="profit_report.xlsx")

    except Exception as e:
        st.error(f"Error loading profit data: {e}")
