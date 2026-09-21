from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
from django.conf import settings

def generate_receipt(partner):
    # Create receipts folder
    receipt_dir = os.path.join(settings.MEDIA_ROOT, 'receipts')
    os.makedirs(receipt_dir, exist_ok=True)

    # Generate receipt number if empty
    if not partner.receipt_number:
        import random
        partner.receipt_number = f"ZGBC-{partner.id:05d}-{random.randint(100,999)}"
        partner.save()

    filename = f"receipt_{partner.receipt_number}.pdf"
    filepath = os.path.join(receipt_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A5)
    width, height = A5

    # Background
    c.setFillColorRGB(0.01, 0.04, 0.18) # #030a2e
    c.rect(0,0,width,height,fill=1)

    # Gold border
    c.setStrokeColorRGB(0.98, 0.64, 0.01) # #faa403
    c.setLineWidth(3)
    c.rect(10,10,width-20,height-20)

    # Title
    c.setFillColorRGB(0.98, 0.64, 0.01)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "ZION GLOBAL BIBLE CHURCH")

    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, height-70, "The Portals' Gate - OFFICIAL RECEIPT")

    # Details
    c.setFont("Helvetica", 11)
    y = height-120
    details = [
        f"Receipt No: {partner.receipt_number}",
        f"Name: {partner.full_name if hasattr(partner, 'full_name') else partner.name}",
        f"Email: {partner.email}",
        f"Phone: {partner.phone}",
        f"Partnership Type: {partner.partnership_type if hasattr(partner, 'partnership_type') else 'Kingdom Partner'}",
        f"Amount: ₦{partner.amount}",
        f"Date: {partner.created_at.strftime('%d %B, %Y')}",
    ]

    for line in details:
        c.drawString(30, y, line)
        y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(0.98, 0.64, 0.01)
    c.drawCentredString(width/2, 80, "2 Corinthians 9:7 - God loves a cheerful giver")

    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 60, "Apostle Henry Leboku Ministries | zionglobalbiblechurch@gmail.com | +2349131245154")

    # Stamp
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.98, 0.64, 0.01)
    c.drawCentredString(width/2, 40, "✓ PAID & BLESSED")

    c.showPage()
    c.save()

    return f"/media/receipts/{filename}", filepath