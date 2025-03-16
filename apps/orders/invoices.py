from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from apps.orders.models import Order


class InvoicePDFGenerator:
    @staticmethod
    def generate(order: Order) -> BytesIO:
        """Generate a PDF invoice for the given order and return it as a buffer."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Header
        elements.append(Paragraph("Invoice", styles["Heading1"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Order ID: {order.id}", styles["Normal"]))
        elements.append(
            Paragraph(f"Customer: {order.customer.email}", styles["Normal"])
        )
        elements.append(
            Paragraph(
                f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
                styles["Normal"],
            )
        )
        elements.append(Spacer(1, 24))

        # Order Items Table
        data = [["Product", "Quantity", "Unit Price", "Total"]]
        for item in order.orderitem_set.all():
            data.append(
                [
                    item.product.name,
                    item.quantity,
                    f"${item.product.price:.2f}",
                    f"${float(item.product.price) * item.quantity:.2f}",
                ]
            )
        data.append(["", "", "Total Amount", f"${order.total_amount:.2f}"])

        table = Table(data, colWidths=[200, 50, 100, 100])
        table.setStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
        elements.append(table)

        # Build PDF into buffer
        doc.build(elements)
        buffer.seek(0)
        return buffer
