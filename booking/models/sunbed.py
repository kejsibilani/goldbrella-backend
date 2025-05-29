from django.core.exceptions import ValidationError
from django.db import models


class SunbedBooking(models.Model):
    booking = models.ForeignKey(
        to='booking.Booking',
        on_delete=models.CASCADE,
        related_name="sunbed_bookings"
    )
    sunbed = models.ForeignKey(
        to='sunbed.Sunbed',
        on_delete=models.CASCADE,
        related_name="sunbed_bookings"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sunbed Bookings"
        verbose_name = "Sunbed Booking"

    def __str__(self):
        return f"Sunbed {self.sunbed.id} booked for {self.booking.user.username}"

    def clean(self):
        # 1) Sunbed must live on the same beach
        if self.sunbed.zone.beach_id != self.booking.beach_id:
            raise ValidationError("Sunbed and Booking must share the same beach.")

        # 2) No double‐booking this sunbed on that date
        is_available = self.sunbed.check_availability(
            booking_date=self.booking.booking_date,
            pk=self.pk
        )
        if not is_available:
            raise ValidationError(
                f"Sunbed {self.sunbed.identity} is already booked on {self.booking.booking_date}."
            )
