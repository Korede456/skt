from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def print_pdf(invoice_number, date, billed_to, payment_info, items, subtotal, vat, ncdmb, grand_total, amount_in_words, filename):
    address = [
    "4th Floor, Lanre Shittu Motors Building, Mabushi, Abuja",
    "FCT, Nigeria.",
    "Email: info@nordatech.com.ng",
    "Phone: +2349041771115"
    ]
    logo_path = "./invoice/utils/logo.png"

    pdf = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Add Logo
    logo_width = 60  # Adjust as necessary
    logo_height = 60  # Adjust as necessary
    pdf.drawImage(logo_path, 50, 700, width=logo_width, height=logo_height, mask='auto')

    # Header
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawString(400, 735, "INVOICE")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(400, 720, f"Invoice No: {invoice_number}")
    pdf.drawString(450, 705, f"Date: {date}")

    # Billed To Section
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 660, "BILLED TO:")
    pdf.setFont("Helvetica", 10)
    y = 645
    for line in billed_to:
        pdf.drawString(50, y, line)
        y -= 15

    # Table Header
    pdf.line(50, y - 45, 550, y - 45)
    y -= 60
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "S/N")
    pdf.drawString(80, y, "ITEM DESCRIPTION")
    pdf.drawString(400, y, "TOTAL COST (₦)")
    pdf.line(50, y - 5, 550, y - 5)

    # Items
    pdf.setFont("Helvetica", 10)
    y -= 20
    for idx, (description, cost) in enumerate(items, start=1):
        pdf.drawString(50, y, str(idx))
        pdf.drawString(80, y, description)
        pdf.drawString(400, y, f"{cost:,.2f}")
        y -= 15

    # Subtotal and Charges
    y -= 10
    pdf.line(50, y, 550, y)

    pdf.drawString(80, y - 15, "Subtotal")
    pdf.drawString(400, y - 15, f"{subtotal:,.2f}")
    pdf.drawString(80, y - 30, "VAT (7.5%)")
    pdf.drawString(400, y - 30, f"{vat:,.2f}")
    pdf.drawString(80, y - 45, "NCDMB (1%)")
    pdf.drawString(400, y - 45, f"{ncdmb:,.2f}")
    pdf.line(50, y - 60, 550, y - 60)
    pdf.drawString(80, y - 75, "GRAND TOTAL")
    pdf.drawString(400, y - 75, f"{grand_total:,.2f}")

    # Payment Information
    labels = ["Bank: ", "Account Name: ", "Account No: ", "Swift Code: ", "Sort Code: ", "TIN: "]
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y - 130, "PAYMENT INFORMATION")
    y -= 145
    for label, line in zip(labels, payment_info):
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y, label)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(150, y, line)
        y -= 15

    # Amount in Words
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y - 10, "Amount in words")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y - 25, amount_in_words)
    # Amount in Words
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y - 10, "Amount in words")
    pdf.setFont("Helvetica", 10)
    words = amount_in_words.split()
    line = ""
    y -= 25
    for word in words:
        if pdf.stringWidth(line + word + " ") < 500:  # 500 - 50 (left margin)
            line += word + " "
        else:
            pdf.drawString(50, y, line.strip())
            line = word + " "
            y -= 15
    if line:
        pdf.drawString(50, y, line.strip())

    # Footer
    y -= 120
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(300, y, "NORDATECH ENERGY LTD")
    pdf.setFont("Helvetica", 10)
    for line in address:
        pdf.drawString(300, y - 15, line)

    pdf.save()