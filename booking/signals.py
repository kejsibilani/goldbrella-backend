from django.db.models.signals import post_save
from django.dispatch import receiver

from booking.models import Booking
from booking.models import BookingToken


@receiver(post_save, sender=Booking)
def create_booking_token(instance, created, **kwargs):
    if created: BookingToken.objects.create(booking=instance)
    return
