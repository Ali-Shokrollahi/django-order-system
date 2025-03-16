from celery import shared_task
from django.core.mail import EmailMessage
from apps.orders.invoices import InvoicePDFGenerator
from apps.orders.repositories import InvoiceRepository, OrderRepository


@shared_task(
    max_retries=3,
    default_retry_delay=60,
    retry_backoff=True,
    retry_jitter=True,
)
def generate_and_save_invoice(order_id: int):
    """Generate and save the invoice PDF for the given order."""

    try:
        order = OrderRepository().get(pk=order_id)
        pdf_buffer = InvoicePDFGenerator.generate(order)
        InvoiceRepository().create_invoice(order, pdf_buffer)
        pdf_buffer.close()
        return f"Invoice generated for Order {order_id}"
    except Exception as e:
        print(f"Error generating invoice for Order {order_id}: {e}")
        generate_and_save_invoice.retry(exc=e)


@shared_task(
    max_retries=3,
    default_retry_delay=60,
    retry_backoff=True,
    retry_jitter=True,
)
def send_order_confirmation_email(order_id, recipient_email):
    try:
        invoice = InvoiceRepository().get_invoice_by_order_id(order_id)

        email = EmailMessage(
            subject=f"Order Confirmation - Order #{order_id}",
            body=f"Thank you for your order! Your order #{order_id} has been placed successfully. See attached invoice.",
            from_email="no-reply@order-system.com",
            to=[recipient_email],
        )
        with invoice.pdf_file.open("rb") as f:
            email.attach(f"invoice_{order_id}.pdf", f.read(), "application/pdf")
        email.send()
        return f"Email sent for Order {order_id}"
    except Exception as e:
        print(f"Error sending email for Order {order_id}: {e}")
        send_order_confirmation_email.retry(exc=e)
