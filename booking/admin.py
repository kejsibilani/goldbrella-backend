from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html
from rest_framework import status
from rest_framework.response import Response

from booking.models import Booking, SunbedBooking
from booking.views.verify import BookingVerificationView
from helpers.qr_utils import generate_booking_qr_code


@admin.register(SunbedBooking)
class SunbedBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'sunbed', 'created')
    list_filter = ('booking__beach', 'booking__booking_date', 'created')
    search_fields = ('booking__user__email', 'sunbed__identity')
    readonly_fields = ('created',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'beach', 'booking_date', 'status', 'created', 'qr_code_link')
    search_fields = ('user__email', 'beach__title', 'token__key')
    list_filter = ('beach', 'status', 'booking_date', 'is_anonymous')
    readonly_fields = ('created', 'updated', 'token', 'qr_code_display')
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'beach', 'booking_date', 'status', 'note')
        }),
        ('System Information', {
            'fields': ('token', 'qr_code_display', 'is_anonymous', 'booked_by', 'created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    
    def qr_code_link(self, obj):
        """Display QR code link in list view"""
        if obj.token:
            return format_html(
                '<a href="{}" target="_blank">View QR Code</a>',
                f'/admin/booking/booking/{obj.id}/qr-code/'
            )
        return "No QR Code"
    qr_code_link.short_description = 'QR Code'
    
    def qr_code_display(self, obj):
        """Display QR code in detail view"""
        if obj.token:
            try:
                qr_data = generate_booking_qr_code(obj)
                return format_html(
                    '<img src="data:image/png;base64,{}" alt="QR Code" style="max-width: 200px;" />'
                    '<br><small>Verification URL: {}</small>',
                    qr_data['qr_code'],
                    qr_data['verification_url']
                )
            except Exception as e:
                return f"Error generating QR code: {str(e)}"
        return "No QR code available"
    qr_code_display.short_description = 'QR Code'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:booking_id>/qr-code/',
                self.admin_site.admin_view(self.qr_code_view),
                name='booking-qr-code',
            ),
            path(
                '<int:booking_id>/verify/',
                self.admin_site.admin_view(self.verify_booking_view),
                name='booking-verify',
            ),
            path(
                'qr-scanner/',
                self.admin_site.admin_view(self.qr_scanner_view),
                name='booking-qr-scanner',
            ),
        ]
        return custom_urls + urls
    
    def qr_code_view(self, request, booking_id):
        """Display QR code for a booking"""
        try:
            booking = Booking.objects.get(id=booking_id)
            if booking.token:
                qr_data = generate_booking_qr_code(booking, request)
                context = {
                    'title': f'QR Code for Booking #{booking.id}',
                    'booking': booking,
                    'qr_data': qr_data,
                }
                return render(request, 'admin/booking/qr_code.html', context)
            else:
                return HttpResponse("No QR code available for this booking", status=400)
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found", status=404)
    
    def verify_booking_view(self, request, booking_id):
        """Verify a booking via admin interface"""
        try:
            booking = Booking.objects.get(id=booking_id)
            if booking.token:
                # Use the verification view logic
                verification_view = BookingVerificationView()
                verification_view.request = request
                response = verification_view.get(request, booking.token.key)
                return HttpResponse(
                    f"Verification result: {response.data}",
                    content_type='application/json',
                    status=response.status_code
                )
            else:
                return HttpResponse("No token available for this booking", status=400)
        except Booking.DoesNotExist:
            return HttpResponse("Booking not found", status=404)
    
    def qr_scanner_view(self, request):
        """Display QR code scanner interface"""
        return render(request, 'admin/booking/qr_scanner.html', {
            'title': 'QR Code Scanner'
        })
