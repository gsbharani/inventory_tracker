from db import get_connection
import pandas as pd
import yagmail

# -------- CRUD ITEMS ----------
def add_item(name, sku, category, purchase_price, selling_price, quantity, supplier, low_stock_threshold):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Items (name, sku, category, purchase_price, selling_price, quantity, supplier, low_stock_threshold)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (name, sku, category, purchase_price, selling_price, quantity, supplier, low_stock_threshold))
    conn.commit()
    conn.close()

def update_item(item_id, name, sku, category, purchase_price, selling_price, supplier, low_stock_threshold):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Items
        SET name=?, sku=?, category=?, purchase_price=?, selling_price=?, supplier=?, low_stock_threshold=?
        WHERE item_id=?""",
        (name, sku, category, purchase_price, selling_price, supplier, low_stock_threshold, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Items WHERE item_id=?", (item_id,))
    conn.commit()
    conn.close()

def get_all_items():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM Items", conn)
    conn.close()
    return df

# -------- STOCK IN / OUT ----------
def stock_in(item_id, qty, notes=''):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Items SET quantity = quantity + ? WHERE item_id=?", (qty, item_id))
    cursor.execute("INSERT INTO StockMovements (item_id, type, quantity, notes) VALUES (?, 'in', ?, ?)", (item_id, qty, notes))
    conn.commit()
    conn.close()

def stock_out(item_id, qty, notes=''):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Items SET quantity = quantity - ? WHERE item_id=?", (qty, item_id))
    cursor.execute("INSERT INTO StockMovements (item_id, type, quantity, notes) VALUES (?, 'out', ?, ?)", (item_id, qty, notes))
    conn.commit()
    conn.close()

# -------- ALERTS ----------
def low_stock_alert():
    conn = get_connection()
    df = pd.read_sql("SELECT name, quantity, low_stock_threshold FROM Items WHERE quantity <= low_stock_threshold", conn)
    conn.close()
    return df

# -------- EXCEL EXPORT ----------
def export_inventory_to_excel(file_path="Inventory_Report.xlsx"):
    df = get_all_items()
    df.to_excel(file_path, index=False)
    return file_path

# -------- EMAIL ALERTS ----------
def send_low_stock_email(recipient_email):
    alerts_df = low_stock_alert()
    if alerts_df.empty:
        return "No low stock items."
    
    message = "Low Stock Alert:\n\n"
    for _, row in alerts_df.iterrows():
        message += f"Item: {row['name']}, Quantity: {row['quantity']}, Threshold: {row['low_stock_threshold']}\n"

    yag = yagmail.SMTP(user="YOUR_EMAIL@gmail.com", password="YOUR_APP_PASSWORD")
    yag.send(to=recipient_email, subject="Inventory Low Stock Alert", contents=message)
    return f"Email sent to {recipient_email}."
