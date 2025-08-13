from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.models import Booking
from booking.choices import BookingStatusChoices
from booking.serializers.read import BookingReadSerializer


class BookingVerificationView(APIView):
    """
    View for verifying bookings via QR code scan
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get(self, request, token_key):
        """
        Verify a booking using the token from QR code
        """
        try:
            booking = get_object_or_404(Booking, token__key=token_key)
            
            # Check if booking is valid
            if booking.status == BookingStatusChoices.CANCELLED.value:
                return Response({
                    'valid': False,
                    'message': 'Booking has been cancelled',
                    'booking': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Serialize booking data
            serializer = BookingReadSerializer(booking)
            
            return Response({
                'valid': True,
                'message': 'Booking verified successfully',
                'booking': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'valid': False,
                'message': 'Invalid booking token',
                'booking': None
            }, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, token_key):
        """
        Mark booking as checked-in/verified
        """
        try:
            booking = get_object_or_404(Booking, token__key=token_key)
            
            # Check if booking is valid
            if booking.status == BookingStatusChoices.CANCELLED.value:
                return Response({
                    'success': False,
                    'message': 'Cannot check in cancelled booking'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update booking status to confirmed if it was reserved
            if booking.status == BookingStatusChoices.RESERVED.value:
                booking.status = BookingStatusChoices.CONFIRMED.value
                booking.save()
            
            serializer = BookingReadSerializer(booking)
            
            return Response({
                'success': True,
                'message': 'Booking checked in successfully',
                'booking': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Invalid booking token'
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def booking_qr_code(request, booking_id):
    """
    Generate QR code for a specific booking
    """
    try:
        booking = get_object_or_404(Booking, id=booking_id)
        
        from helpers.qr_utils import generate_booking_qr_code
        
        qr_data = generate_booking_qr_code(booking, request)
        
        return Response({
            'booking_id': booking.id,
            'qr_code': qr_data['qr_code'],
            'verification_url': qr_data['verification_url'],
            'token': qr_data['token']
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND) 