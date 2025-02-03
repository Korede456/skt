from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_waybill(waybill_number, company_info, dispatch_info, receiving_info, filename):
    pdf = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Header: Company Information
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 750, f"Waybill Number: {waybill_number}")
    pdf.setFont("Helvetica", 10)
    y = 730
    for line in company_info:
        pdf.drawString(50, y, line)
        y -= 15

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(220, y - 10, "WAYBILL")
    y -= 40

    # Dispatch Section
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "DISPATCH SECTION")
    pdf.setFont("Helvetica", 10)
    y -= 20
    for key, value in dispatch_info.items():
        pdf.drawString(50, y, f"{key}: {value}")
        y -= 15

    # Table Header for Dispatch Section
    y -= 20
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "Commodity")
    pdf.drawString(150, y, "Shipment #")
    pdf.drawString(250, y, "Unit Type")
    pdf.drawString(350, y, "Unit Weight")
    pdf.drawString(450, y, "Total Qty")
    pdf.line(50, y - 5, 550, y - 5)

    # Receiving Section
    y -= 40
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "RECEIVING SECTION")
    pdf.setFont("Helvetica", 10)
    y -= 20
    for key, value in receiving_info.items():
        pdf.drawString(50, y, f"{key}: {value}")
        y -= 15

    # Table Header for Receiving Section
    y -= 20
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "Commodity")
    pdf.drawString(150, y, "Shipment #")
    pdf.drawString(250, y, "Unit Type")
    pdf.drawString(350, y, "Unit Weight")
    pdf.drawString(450, y, "Short/Excess Qty")
    pdf.line(50, y - 5, 550, y - 5)

    # Footer: Driver and Signatures
    y -= 40
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, "Driver's Name: __________________________")
    pdf.drawString(300, y, "Received by: __________________________")
    y -= 20
    pdf.drawString(50, y, "Driving License/Permit #: _______________")
    pdf.drawString(300, y, "Title: _________________________________")
    y -= 20
    pdf.drawString(50, y, "Signature and Date: _____________________")
    pdf.drawString(300, y, "Signature and Date: _____________________")

    # Save PDF
    pdf.save()

# Example Usage
company_info = [
    "4th Floor Lanre Shittu Motors Building, Shehu Yaradua Way, Mabushi, Abuja FCT.",
    "Telephone: +234(0)9041771115",
    "Email: info@nordatech.com.ng",
    "Website: www.nordatech.com.ng"
]

dispatch_info = {
    "From": "Warehouse A",
    "To": "Warehouse B",
    "Date": "2025-01-18",
    "Authorization #": "12345",
    "Consignee": "John Doe",
    "Truck # / Trailer #": "ABC-1234"
}

receiving_info = {
    "Commodity": "Oil Drums",
    "Shipment #": "56789",
    "Unit Type": "Drum",
    "Unit Weight": "200kg",
    "Total Qty": "100"
}

create_waybill(
    waybill_number="NTE001NSR",
    company_info=company_info,
    dispatch_info=dispatch_info,
    receiving_info=receiving_info,
    filename="Waybill.pdf"
)
