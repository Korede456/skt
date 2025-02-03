from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def create_invoice_with_logo(invoice_number, date, billed_to, payment_info, items, subtotal, vat, ncdmb, grand_total, amount_in_words, filename):
    address = [
    "4th Floor, Lanre Shittu Motors Building, Mabushi, Abuja",
    "FCT, Nigeria.",
    "Email: info@nordatech.com.ng",
    "Phone: +2349041771115"
    ]
    logo_path="./invoice/utils/logo.png", 
    
    pdf = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Add Logo
    logo_width = 150  # Adjust as necessary
    logo_height = 50  # Adjust as necessary
    pdf.drawImage(logo_path, 50, 710, width=logo_width, height=logo_height, mask='auto')

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
    pdf.drawString(400, y, "TOTAL COST ($)")
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
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y - 130, "PAYMENT INFORMATION")
    y -= 145
    pdf.setFont("Helvetica", 10)
    for line in payment_info:
        pdf.drawString(50, y, line)
        y -= 15

    # Amount in Words
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y - 10, "Amount in words")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y - 25, amount_in_words)

    # Footer
    y -= 120
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(300, y, "NORDATECH ENERGY LTD")
    pdf.setFont("Helvetica", 10)
    for line in address:
        pdf.drawString(300, y - 15, line)
        y -= 15

    # Save PDF
    pdf.save()

# Example Usage
billed_to = [
    "Aquarian Oil & Gas Limited",
    "17A Layi-Ajayi Bembe Road, Parkview,",
    "Ikoyi, Lagos, Nigeria."
]

payment_info = [
    "Sterling Bank Plc",
    "Account Name: Nordatech Energy Ltd",
    "Account No.: 0094466145",
    "Swift Code: NAMENGLA",
    "Sort Code: 232080092",
    "TIN: 23907427-0001"
]

items = [
    ("Completion of Pilot Hole and 17 1/2\" First Hole Section", 232240.07),
    ("Less 40% Billed in Naira", -92896.03)
]

create_invoice_with_logo(
    invoice_number="AOG/ME/02403USD",
    date="13 March, 2024",
    billed_to=billed_to,
    payment_info=payment_info,
    items=items,
    subtotal=139344.04,
    vat=10450.80,
    ncdmb=1393.44,
    grand_total=151188.29,
    amount_in_words="One Hundred and Fifty-One Thousand, One Hundred and Eighty-Eight Dollars, Twenty-Nine Cents Only.",
    filename="Invoice_with_Logo.pdf",
)
