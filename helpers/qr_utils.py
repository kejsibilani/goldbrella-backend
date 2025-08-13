import qrcode
import base64
import io
from django.conf import settings
from django.urls import reverse
from django.http import HttpRequest


def generate_booking_qr_code(booking, request=None):
    """
    Generate QR code for a booking that can be scanned by admin
    """
    # Create the booking verification URL
    if request:
        base_url = f"{request.scheme}://{request.get_host()}"
    else:
        base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    
    verification_url = f"{base_url}/api/v1/bookings/verify/{booking.token.key}/"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(verification_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        'qr_code': img_str,
        'verification_url': verification_url,
        'booking_id': booking.id,
        'token': booking.token.key
    }


def generate_booking_qr_code_file(booking, filename=None):
    """
    Generate QR code file for a booking
    """
    if not filename:
        filename = f"booking_{booking.id}_qr.png"
    
    # Create the booking verification URL
    base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    verification_url = f"{base_url}/api/v1/bookings/verify/{booking.token.key}/"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(verification_url)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to file
    img.save(filename)
    
    return {
        'filename': filename,
        'verification_url': verification_url,
        'booking_id': booking.id,
        'token': booking.token.key
    } 