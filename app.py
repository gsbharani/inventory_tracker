import streamlit as st
import pandas as pd
from db import get_connection, create_tables
from invoice import generate_invoice
from email_alerts import send_email
from whatsapp_alerts import send_whatsapp

st.set_page_config(page_title="Inventory SaaS", layout="wide")
create_tables()
conn = get_connection()

menu = st.sidebar.selectbox(
    "Menu",
    ["Dashboard", "Inventory", "Sales", "Purchase", "Profit Report", "Pricing"]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.title("📊 Business Dashboard")

    items = pd.read_sql("SELECT * FROM items", conn)
    sales = pd.read_sql("SELECT * FROM sales", conn)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Items", len(items))
    col2.metric("Total Stock", items["quantity"].sum())
    col3.metric("Total Sales ₹", sales["total"].sum() if not sales.empty else 0)

    st.bar_chart(items.set_index("item_name")["quantity"])

# ---------------- INVENTORY ----------------
elif menu == "Inventory":
    st.title("📦 Inventory")

    with st.form("add_item"):
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("Item Name")
        cat = c2.text_input("Category")
        qty = c3.number_input("Qty", 0)
        cost = c1.number_input("Cost Price", 0.0)
        sell = c2.number_input("Selling Price", 0.0)
        min_stock = c3.number_input("Min Stock", 1)

        if st.form_submit_button("Add"):
            conn.execute(
                "INSERT INTO items VALUES (NULL,?,?,?,?,?,?)",
                (name, cat, qty, cost, sell, min_stock)
            )
            conn.commit()
            st.success("Item added")

    df = pd.read_sql("SELECT * FROM items", conn)
    st.dataframe(df, use_container_width=True)

# ---------------- SALES ----------------
elif menu == "Sales":
    st.title("🧾 Sales")

    items = pd.read_sql("SELECT * FROM items", conn)
    item = st.selectbox("Item", items["item_name"])
    qty = st.number_input("Qty", 1)
    customer = st.text_input("Customer")

    if st.button("Record Sale"):
        row = items[items["item_name"] == item].iloc[0]
        total = qty * row["selling_price"]

        conn.execute(
            "INSERT INTO sales VALUES (NULL,?,?,?,?,?,CURRENT_DATE)",
            (row["item_id"], qty, row["selling_price"], total, customer)
        )
        conn.execute(
            "UPDATE items SET quantity = quantity - ? WHERE item_id=?",
            (qty, row["item_id"])
        )
        conn.commit()

        pdf = generate_invoice(1, customer, item, qty, row["selling_price"])
        st.success("Sale recorded & invoice generated")

# ---------------- PURCHASE ----------------
elif menu == "Purchase":
    st.title("📥 Purchase")

    items = pd.read_sql("SELECT * FROM items", conn)
    item = st.selectbox("Item", items["item_name"])
    qty = st.number_input("Qty Purchased", 1)
    vendor = st.text_input("Vendor")

    if st.button("Record Purchase"):
        row = items[items["item_name"] == item].iloc[0]
        total = qty * row["cost_price"]

        conn.execute(
            "INSERT INTO purchases VALUES (NULL,?,?,?,?,?,CURRENT_DATE)",
            (row["item_id"], qty, row["cost_price"], total, vendor)
        )
        conn.execute(
            "UPDATE items SET quantity = quantity + ? WHERE item_id=?",
            (qty, row["item_id"])
        )
        conn.commit()
        st.success("Purchase recorded")

# ---------------- DAILY PROFIT REPORT ----------------
elif menu == "Profit Report":
    st.title("📈 Daily Profit Report")

    query = """
    SELECT 
        s.sale_date,
        SUM(s.total) AS sales_amount,
        SUM(s.qty * i.cost_price) AS cost_amount,
        SUM(s.total) - SUM(s.qty * i.cost_price) AS profit
    FROM sales s
    JOIN items i ON s.item_id = i.item_id
    GROUP BY s.sale_date
    """

    report = pd.read_sql(query, conn)
    st.dataframe(report, use_container_width=True)

    st.line_chart(report.set_index("sale_date")["profit"])

    if not report.empty:
        today_profit = report.iloc[-1]["profit"]
        if today_profit < 0:
            send_email("⚠️ Today profit is negative")
            send_whatsapp("⚠️ Alert: Today profit is negative")

# ---------------- PRICING ----------------
elif menu == "Pricing":
    st.title("💰 Pricing Plans")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Basic\n₹499/month\n✔ Inventory\n✔ Excel Export")
    with c2:
        st.markdown("### Pro\n₹999/month\n✔ Sales & Purchase\n✔ PDF Invoice\n✔ Profit Report")
    with c3:
        st.markdown("### Enterprise\nCustom\n✔ WhatsApp Alerts\n✔ Custom Reports\n✔ Cloud DB")
