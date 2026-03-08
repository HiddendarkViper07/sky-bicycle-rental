# booking/utils.py
import razorpay
from django.conf import settings
import hashlib
import hmac
import json

def create_razorpay_order(amount, receipt_id):
    """Create Razorpay order"""
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    
    order_data = {
        'amount': amount * 100,  # Convert to paise
        'currency': 'INR',
        'receipt': receipt_id,
        'payment_capture': 1
    }
    
    try:
        order = client.order.create(order_data)
        return order
    except Exception as e:
        print(f"Razorpay error: {e}")
        return None

def verify_payment_signature(order_id, payment_id, signature):
    """Verify Razorpay payment signature"""
    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    
    try:
        client.utility.verify_payment_signature(params_dict)
        return True
    except:
        return False

def generate_receipt_text(booking):
    """Generate receipt text for download"""
    receipt = f"""
===========================================
           SKY BICYCLE RENTAL
            BOOKING TICKET
===========================================

Ticket No: {booking.ticket_id}
Date: {booking.created_at.strftime('%d-%m-%Y %H:%M')}

-------------------------------------------
CUSTOMER DETAILS
-------------------------------------------
Name: {booking.full_name}
Mobile: {booking.mobile}
Aadhar: XXX-XXXX-{booking.aadhar_number[-4:]}

-------------------------------------------
RENTAL DETAILS
-------------------------------------------
Date: {booking.rent_date}
Time: {booking.rent_time}
Duration: {booking.hours} hours
Location: {booking.location[:50]}

-------------------------------------------
PAYMENT DETAILS
-------------------------------------------
Total Amount: ₹{booking.total_amount}
Paid Now: ₹{booking.paid_amount}
Balance Due: ₹{booking.balance_amount}
Payment ID: {booking.payment_id or 'N/A'}

-------------------------------------------
STATUS: {booking.status.upper()}
-------------------------------------------

Please show this ticket at the time of pickup.
Valid only on booking date.

Thank you for choosing Sky Bicycle Rental!
===========================================
    """
    return receipt