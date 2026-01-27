import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

def dashboard_page():
    st.header("📊 Business Dashboard")

    conn = get_connection()

    kpi = pd.read_sql("""
        SELECT
            COUNT(DISTINCT i.item_id) AS items,
            COALESCE(SUM(i.quantity),0) AS stock,
            ROUND(COALESCE(SUM(s.total_amount), 0) / 100000.0, 2) AS sales
        FROM items i
        LEFT JOIN sales s ON i.vendor_id=s.vendor_id
        WHERE i.vendor_id=%s
    """, conn, params=(st.session_state.vendor_id,))

    profit = pd.read_sql("""
        SELECT COALESCE(SUM((i.selling_price - i.purchase_price) * s.quantity),0) AS profit
        FROM sales s
        JOIN items i ON s.item_id=i.item_id
        WHERE s.vendor_id=%s
    """, conn, params=(st.session_state.vendor_id,))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Items", int(kpi["items"][0]))
    c2.metric("Total Stocks", int(kpi["stock"][0]))
    c3.metric("Total Sales", f"₹ {kpi['sales'][0]:.2f} Lakhs")
    c4.metric("Profit", f"₹ {profit['profit'][0]}")

    sales_chart = pd.read_sql("""
    SELECT DATE(created_at) AS day,
           SUM(total_amount) AS sales
    FROM sales
    WHERE vendor_id = %s
    GROUP BY day
    ORDER BY day
""", conn, params=(st.session_state.vendor_id,))

if not sales_chart.empty:
    # Fix date issue
    sales_chart["day"] = pd.to_datetime(sales_chart["day"]).dt.date

    fig = px.line(
        sales_chart,
        x="day",
        y="sales",
        title="Daily Sales",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales (₹)",
        xaxis=dict(type="category")
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No sales data available")

conn.close()

