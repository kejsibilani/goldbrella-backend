from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import localdate
from simple_history.models import HistoricalRecords

from booking.choices import BookingStatusChoices


class Booking(models.Model):
    _history = HistoricalRecords(related_name="history")

    beach = models.ForeignKey(
        to='beach.Beach',
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booking_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=BookingStatusChoices.choices,
        default=BookingStatusChoices.RESERVED.value
    )

    sunbeds = models.ManyToManyField(
        to='sunbed.Sunbed',
        related_name="bookings",
        through="booking.SunbedBooking"
    )

    user = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    booked_by = models.ForeignKey(
        to='account.User',
        on_delete=models.SET_NULL,
        related_name="booked_bookings",
        blank=True, null=True
    )

    note = models.TextField(blank=True, null=True)
    is_anonymous = models.BooleanField(
        help_text='Booking generated anonymously',
        default=False
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Bookings"
        verbose_name = "Booking"

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} at {self.beach.title} on {self.booking_date}"

    def clean(self):
        # —————————————————————————————————————————————
        # 1) No past-date bookings
        # —————————————————————————————————————————————
        if not self.pk and self.booking_date < localdate():
            raise ValidationError({'booking_date': "Cannot book a past date."})

        # —————————————————————————————————————————————
        # 2) Beach is immutable once created
        # —————————————————————————————————————————————
        if self.pk:
            orig = Booking.objects.get(pk=self.pk)
            if orig.beach_id != self.beach_id:
                raise ValidationError({'beach': "You cannot change the beach for an existing booking."})

        # —————————————————————————————————————————————
        # 3) Sunbeds must belong to this beach & not already booked on this date
        # —————————————————————————————————————————————
        errors = {}
        for sb in (self.sunbeds.all() if self.pk else self.sunbeds.model.objects.filter(bookings=self)):
            if sb.zone.beach_id != self.beach_id:
                errors.setdefault('sunbeds', []).append(
                    f"Sunbed #{sb.id} does not belong to beach “{self.beach.title}”."
                )

            conflict_qs = self.sunbeds.through.objects.filter(
                booking__booking_date=self.booking_date,
                booking__status__in=[
                    BookingStatusChoices.PARTIAL_RESERVED.value,
                    BookingStatusChoices.CONFIRMED.value,
                    BookingStatusChoices.RESERVED.value
                ],
                sunbed__in=self.sunbeds.all(),
            )
            if self.pk:
                conflict_qs = conflict_qs.exclude(booking=self)
            if conflict_qs.exists():
                errors.setdefault('sunbeds', []).append(
                    "One or more sunbeds are already booked for this date."
                )

        if errors:
            raise ValidationError(errors)
