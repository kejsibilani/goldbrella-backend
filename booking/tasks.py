from celery import shared_task

from booking.choices import BookingStatusChoices
from booking.models import Booking


@shared_task(bind=True)
def cancel_partial_bookings(self, booking_id):
    """
    Runs ~30 minutes after reservation. If booking is still 'reserved',
    mark it 'cancelled'. Otherwise (already 'confirmed'), do nothing.
    """

    try:
        booking = Booking.objects.select_for_update().get(pk=booking_id)
    except Booking.DoesNotExist:
        # Booking was deleted or never existed; nothing to do.
        return

    # Only cancel if still reserved
    if booking.status == BookingStatusChoices.PARTIAL_RESERVED.value:
        booking.status = BookingStatusChoices.CANCELLED.value
        booking.save(update_fields=["status"])
    return
