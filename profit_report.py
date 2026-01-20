import streamlit as st
import pandas as pd
from db import get_connection

def profit_report():
    st.subheader("Daily Profit Report")

    conn = get_connection()

    sales = pd.read_sql("""
        SELECT date, SUM(total) AS sales_amount
        FROM sales
        WHERE vendor_id=?
        GROUP BY date
    """, conn, params=(st.session_state.vendor_id,))

    purchases = pd.read_sql("""
        SELECT date, SUM(total_cost) AS purchase_amount
        FROM purchases
        WHERE vendor_id=?
        GROUP BY date
    """, conn, params=(st.session_state.vendor_id,))

    df = sales.merge(purchases, on="date", how="left").fillna(0)
    df["profit"] = df["sales_amount"] - df["purchase_amount"]

    st.dataframe(df)
    st.metric("Total Profit", df["profit"].sum())

    conn.close()
