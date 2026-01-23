from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_invoice(filename):
    c = canvas.Canvas(filename, pagesize=A4)
    c.drawString(100, 800, "INVOICE")
    c.save()
