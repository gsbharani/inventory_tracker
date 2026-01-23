import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection

def analytics_page():
    st.header("📈 Analytics")

    conn = get_connection()

    top_items = pd.read_sql("""
        SELECT i.item_name, SUM(s.quantity) AS sold
        FROM sales s
        JOIN items i ON s.item_id=i.item_id
        WHERE s.vendor_id=%s
        GROUP BY i.item_name
        ORDER BY sold DESC
        LIMIT 5
    """, conn, params=(st.session_state.vendor_id,))

    if not top_items.empty:
        fig = px.bar(top_items, x="item_name", y="sold", title="Top Selling Items")
        st.plotly_chart(fig, use_container_width=True)

    conn.close()
