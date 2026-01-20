import streamlit as st
import pandas as pd
from db import get_connection, create_tables

create_tables()
conn = get_connection()

st.set_page_config(page_title="Inventory SaaS", layout="wide")
st.title("📦 Inventory Management SaaS")

menu = st.sidebar.radio(
    "Menu",
    ["Add Item", "Sales", "Purchase", "Dashboard", "Admin DB Access"]
)

# ---------------- ADD ITEM ----------------
if menu == "Add Item":
    st.subheader("Add New Item")

    name = st.text_input("Item Name")
    category = st.text_input("Category")
    qty = st.number_input("Quantity", 0)
    price = st.number_input("Price", 0.0)

    if st.button("Save Item"):
        conn.execute(
            "INSERT INTO items (name, category, quantity, price) VALUES (?,?,?,?)",
            (name, category, qty, price)
        )
        conn.commit()
        st.success("Item Added")

# ---------------- SALES ----------------
elif menu == "Sales":
    st.subheader("Sales Entry")

    items = pd.read_sql("SELECT * FROM items", conn)
    item = st.selectbox("Item", items["name"])
    qty = st.number_input("Quantity Sold", 1)

    if st.button("Save Sale"):
        item_row = items[items["name"] == item].iloc[0]
        total = qty * item_row["price"]

        conn.execute(
            "INSERT INTO sales (item_id, qty, total) VALUES (?,?,?)",
            (item_row["id"], qty, total)
        )

        conn.execute(
            "UPDATE items SET quantity = quantity - ? WHERE id = ?",
            (qty, item_row["id"])
        )

        conn.commit()
        st.success("Sale Recorded")

# ---------------- PURCHASE ----------------
elif menu == "Purchase":
    st.subheader("Purchase Entry")

    items = pd.read_sql("SELECT * FROM items", conn)
    item = st.selectbox("Item", items["name"])
    qty = st.number_input("Quantity Purchased", 1)
    cost = st.number_input("Cost per unit", 0.0)

    if st.button("Save Purchase"):
        item_row = items[items["name"] == item].iloc[0]

        conn.execute(
            "INSERT INTO purchases (item_id, qty, cost) VALUES (?,?,?)",
            (item_row["id"], qty, cost)
        )

        conn.execute(
            "UPDATE items SET quantity = quantity + ? WHERE id = ?",
            (qty, item_row["id"])
        )

        conn.commit()
        st.success("Purchase Recorded")

# ---------------- DASHBOARD ----------------
elif menu == "Dashboard":
    st.subheader("📊 Dashboard")

    items = pd.read_sql("SELECT * FROM items", conn)
    sales = pd.read_sql("SELECT * FROM sales", conn)

    st.metric("Total Items", len(items))
    st.metric("Total Sales Amount", sales["total"].sum() if not sales.empty else 0)

    st.dataframe(items)

# ---------------- ADMIN DB ACCESS ----------------
elif menu == "Admin DB Access":
    st.subheader("🛠 Database Access (ADMIN)")

    st.markdown("### Run SQL Query")
    query = st.text_area("SQL Query", "SELECT * FROM items")

    if st.button("Execute Query"):
        try:
            df = pd.read_sql(query, conn)
            st.dataframe(df)
        except Exception as e:
            st.error(e)

    st.markdown("### Download Database")

    with open("inventory.db", "rb") as f:
        st.download_button(
            "Download inventory.db",
            f,
            file_name="inventory.db"
        )
