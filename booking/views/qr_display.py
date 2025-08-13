from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from booking.models import Booking
from helpers.qr_utils import generate_booking_qr_code


@login_required
def booking_qr_display(request, booking_id):
    """
    Display QR code for a booking to the user
    """
    try:
        # Get booking and ensure user owns it or is staff
        if request.user.is_staff:
            booking = get_object_or_404(Booking, id=booking_id)
        else:
            booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        # Generate QR code data
        qr_data = generate_booking_qr_code(booking, request)
        
        context = {
            'booking': booking,
            'qr_data': qr_data,
        }
        
        return render(request, 'booking/qr_code.html', context)
        
    except Exception as e:
        raise Http404("Booking not found or access denied")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_qr_api(request, booking_id):
    """
    API endpoint to get QR code data for a booking
    """
    try:
        # Get booking and ensure user owns it or is staff
        if request.user.is_staff:
            booking = get_object_or_404(Booking, id=booking_id)
        else:
            booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        
        # Generate QR code data
        qr_data = generate_booking_qr_code(booking, request)
        
        return Response({
            'booking_id': booking.id,
            'qr_code': qr_data['qr_code'],
            'verification_url': qr_data['verification_url'],
            'token': qr_data['token']
        })
        
    except Exception as e:
        return Response({
            'error': 'Booking not found or access denied'
        }, status=404) 