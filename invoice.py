from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_invoice(invoice_no, customer, item, qty, price):
    filename = f"invoice_{invoice_no}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, "INVOICE")

    c.setFont("Helvetica", 10)
    c.drawString(50, 770, f"Invoice No: {invoice_no}")
    c.drawString(50, 750, f"Customer: {customer}")

    c.drawString(50, 700, f"Item: {item}")
    c.drawString(50, 680, f"Quantity: {qty}")
    c.drawString(50, 660, f"Price: ₹{price}")
    c.drawString(50, 640, f"Total: ₹{qty * price}")

    c.save()
    return filename
