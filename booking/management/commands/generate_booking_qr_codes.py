from django.core.management.base import BaseCommand
from django.db import transaction
from booking.models import Booking, BookingToken
from helpers.qr_utils import generate_booking_qr_code_file
import os


class Command(BaseCommand):
    help = 'Generate QR codes for existing bookings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='qr_codes',
            help='Output directory for QR code files'
        )
        parser.add_argument(
            '--booking-id',
            type=int,
            help='Generate QR code for specific booking ID'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate QR codes even if they exist'
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']
        booking_id = options['booking_id']
        force = options['force']

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        if booking_id:
            # Generate QR code for specific booking
            try:
                booking = Booking.objects.get(id=booking_id)
                self.generate_qr_for_booking(booking, output_dir, force)
            except Booking.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Booking with ID {booking_id} not found')
                )
        else:
            # Generate QR codes for all bookings
            bookings = Booking.objects.all()
            self.stdout.write(f'Generating QR codes for {bookings.count()} bookings...')

            for booking in bookings:
                self.generate_qr_for_booking(booking, output_dir, force)

            self.stdout.write(
                self.style.SUCCESS('QR code generation completed!')
            )

    def generate_qr_for_booking(self, booking, output_dir, force):
        """Generate QR code for a specific booking"""
        filename = f"booking_{booking.id}_qr.png"
        filepath = os.path.join(output_dir, filename)

        # Check if file already exists
        if os.path.exists(filepath) and not force:
            self.stdout.write(
                f'QR code for booking {booking.id} already exists: {filepath}'
            )
            return

        try:
            # Ensure booking has a token
            if not hasattr(booking, 'token'):
                with transaction.atomic():
                    BookingToken.objects.get_or_create(booking=booking)
                self.stdout.write(f'Created token for booking {booking.id}')

            # Generate QR code
            qr_data = generate_booking_qr_code_file(booking, filepath)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Generated QR code for booking {booking.id}: {filepath}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error generating QR code for booking {booking.id}: {str(e)}'
                )
            ) 