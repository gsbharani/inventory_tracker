import streamlit as st
import pandas as pd
import plotly.express as px
from models import get_all_items, low_stock_alert, export_inventory_to_excel, send_low_stock_email, add_item, update_item, delete_item, stock_in, stock_out

st.set_page_config(page_title="Inventory Tracker SaaS", layout="wide")
st.title("📦 Inventory Tracker SaaS")

menu = ["Dashboard", "Manage Items", "Stock In/Out"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- DASHBOARD ----------------
if choice == "Dashboard":
    df = get_all_items()
    st.subheader("📊 Current Inventory")
    st.dataframe(df)

    st.subheader("⚠️ Low Stock Alerts")
    alerts = low_stock_alert()
    if alerts.empty:
        st.success("All items have sufficient stock.")
    else:
        st.warning(alerts)

    st.subheader("📈 Stock Quantity Chart")
    fig = px.bar(df, x="name", y="quantity", color="category", title="Stock Quantity by Item")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("💾 Export Inventory to Excel")
    if st.button("Export Excel"):
        file_path = export_inventory_to_excel()
        st.success(f"Excel file created: {file_path}")
        st.download_button("Download Excel", file_path)

    st.subheader("📧 Send Low Stock Email Alert")
    email = st.text_input("Enter Email", "")
    if st.button("Send Email Alert"):
        if email:
            result = send_low_stock_email(email)
            st.success(result)
        else:
            st.error("Enter email.")

# ---------------- MANAGE ITEMS ----------------
elif choice == "Manage Items":
    st.subheader("Add New Item")
    with st.form(key="add_item_form"):
        name = st.text_input("Item Name")
        sku = st.text_input("SKU")
        category = st.text_input("Category")
        purchase_price = st.number_input("Purchase Price")
        selling_price = st.number_input("Selling Price")
        quantity = st.number_input("Quantity", min_value=0)
        supplier = st.text_input("Supplier")
        low_stock_threshold = st.number_input("Low Stock Threshold", min_value=0)
        submit = st.form_submit_button("Add Item")
        if submit:
            add_item(name, sku, category, purchase_price, selling_price, quantity, supplier, low_stock_threshold)
            st.success(f"Item {name} added successfully!")

    st.subheader("Update / Delete Item")
    df = get_all_items()
    selected_item = st.selectbox("Select Item", df['item_id'])
    item_data = df[df['item_id'] == selected_item].iloc[0]

    with st.form(key="update_item_form"):
        name = st.text_input("Item Name", item_data['name'])
        sku = st.text_input("SKU", item_data['sku'])
        category = st.text_input("Category", item_data['category'])
        purchase_price = st.number_input("Purchase Price", value=float(item_data['purchase_price']))
        selling_price = st.number_input("Selling Price", value=float(item_data['selling_price']))
        supplier = st.text_input("Supplier", item_data['supplier'])
        low_stock_threshold = st.number_input("Low Stock Threshold", value=int(item_data['low_stock_threshold']))
        update_submit = st.form_submit_button("Update Item")
        delete_submit = st.form_submit_button("Delete Item")
        if update_submit:
            update_item(selected_item, name, sku, category, purchase_price, selling_price, supplier, low_stock_threshold)
            st.success(f"Item {name} updated successfully!")
        if delete_submit:
            delete_item(selected_item)
            st.success(f"Item {name} deleted successfully!")

# ---------------- STOCK IN/OUT ----------------
elif choice == "Stock In/Out":
    df = get_all_items()
    selected_item = st.selectbox("Select Item", df['item_id'])
    item_data = df[df['item_id'] == selected_item].iloc[0]

    st.subheader(f"Update Stock for {item_data['name']}")
    qty = st.number_input("Quantity", min_value=1)
    notes = st.text_area("Notes")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Stock In"):
            stock_in(selected_item, qty, notes)
            st.success(f"Added {qty} to {item_data['name']}")
    with col2:
        if st.button("Stock Out"):
            stock_out(selected_item, qty, notes)
            st.success(f"Removed {qty} from {item_data['name']}")
