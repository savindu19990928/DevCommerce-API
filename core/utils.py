import logging
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)

def log_action(description: str, user=None, order=None):
    from .models import AuditLog
    AuditLog.objects.create(
        action_description=description,
        user=user,
        related_order=order
    )

def process_dummy_payment(amount: float, order_id: str, payment_method: str = 'paypal'):
    """
    Dummy payment gateway action as requested.
    Always returns success for testing purposes.
    """
    logger.info(f"Processing dummy payment: Order {order_id}, Amount: {amount}, Method: {payment_method}")
    # In a real scenario, this would call PayPal SDK.
    return {
        "status": "success",
        "transaction_id": f"dummy_txn_{order_id}_{amount}",
        "amount_paid": amount
    }

def send_dummy_sms(phone_number: str, message: str):
    """
    Dummy SMS action.
    """
    logger.info(f"Sending dummy SMS to {phone_number}: {message}")
    return True

def send_dummy_email(email_address: str, subject: str, message: str, html_message: str = None):
    """
    Dummy email action.
    """
    logger.info(f"Sending dummy email to {email_address} | Subject: {subject}")
    # Using Django's default mailer for real sending, but logging here as dummy.
    # We could also use django.core.mail.send_mail here.
    return True

def generate_receipt_pdf(order):
    """
    Generates a PDF receipt for a given Order object.
    Returns the PDF as a bytes object.
    """
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, "DevCommerce Receipt")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, 720, f"Order Number: {order.order_number}")
    p.drawString(50, 700, f"Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(50, 680, f"Status: {order.status}")
    
    y = 640
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Items:")
    y -= 20
    
    p.setFont("Helvetica", 12)
    for item in order.items.all():
        p.drawString(70, y, f"{item.quantity}x {item.product.name} - ${item.subtotal}")
        y -= 20
        
    p.line(50, y-10, 550, y-10)
    y -= 30
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Total: ${order.total}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer.read()
