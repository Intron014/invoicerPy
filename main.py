from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


def create_invoice(items, tax_types, tax_names, inv_name="Invoice", signature_line=False):
    currency_symbol = "$"
    pdf_file = "invoice.pdf"
    pdf = canvas.Canvas(pdf_file, pagesize=letter)

    logo_path = "input/logo.png"  # Path to the logo
    logo = ImageReader(logo_path)
    pdf.drawImage(logo, 50, 730, width=50, height=50)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 715, inv_name)

    y = 670
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, 695, "Item")
    pdf.drawString(200, 695, "Quantity")
    pdf.drawString(300, 695, "Price")
    pdf.drawString(400, 695, "Total")
    pdf.line(50, y + 20, 550, y + 20)

    subtotal = 0
    taxes = {}

    for item in items:
        pdf.drawString(50, y, item['name'])
        pdf.drawString(200, y, str(item['quantity']))
        pdf.drawString(300, y, "{}{:.2f}".format(currency_symbol, item['price']))

        total = item['quantity'] * item['price']
        subtotal += total
        pdf.drawString(400, y, "{}{:.2f}".format(currency_symbol, total))

        tax_rate = tax_types[item['tax_id']]
        tax_amount = total * tax_rate
        if item['tax_id'] in taxes:
            taxes[item['tax_id']] += tax_amount
        else:
            taxes[item['tax_id']] = tax_amount

        y -= 20

    # Draw line separator
    pdf.line(50, y + 10, 550, y + 10)

    # Add subtotal
    pdf.drawString(300, y - 10, "Subtotal:")
    pdf.drawString(400, y - 10, "{}{:.2f}".format(currency_symbol, subtotal))

    # Add taxes
    y -= 30
    for tax_id, tax_amount in taxes.items():
        tax_rate = tax_types[tax_id]
        tax_name = tax_names[tax_id]
        pdf.drawString(300, y, f"{tax_name} ({tax_rate * 100}%):")
        pdf.drawString(400, y, "{}{:.2f}".format(currency_symbol, tax_amount))
        y -= 20

    total_amount = subtotal + sum(taxes.values())
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(300, y - 10, "Total:")
    pdf.drawString(400, y - 10, "{}{:.2f}".format(currency_symbol, total_amount))

    if signature_line:
        pdf.line(50, 150, 250, 150)
        pdf.drawString(50, 135, "Signature")

    pdf.save()
    print(f"Invoice created: {pdf_file}")


def get_tax_types_from_user():
    tax_types = {}
    tax_names = {}
    while True:
        tax_id = input("Enter tax ID (or 'done' to finish): ")
        if tax_id.lower() == 'done':
            break
        tax_names[tax_id] = input("Enter Tax Name: ")
        tax_percentage = float(input("Enter tax percentage: "))
        tax_types[tax_id] = tax_percentage / 100

    return tax_types, tax_names


def get_items_from_user():
    items = []
    while True:
        item_name = input("Enter item name (or 'done' to finish): ")
        if item_name.lower() == 'done':
            break

        item_quantity = int(input("Enter quantity: "))
        item_price = float(input("Enter price: "))
        item_tax_id = input("Enter tax ID: ")

        item = {"name": item_name, "quantity": item_quantity, "price": item_price, "tax_id": item_tax_id}
        items.append(item)

    return items


o_tax_types, o_tax_names = get_tax_types_from_user()
o_items = get_items_from_user()
create_invoice(o_items, o_tax_types, o_tax_names)
