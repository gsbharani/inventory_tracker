from db import get_connection

def login(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT vendor_id, name FROM vendors WHERE email=%s AND password=%s",
        (email, password)
    )
    return cur.fetchone()

