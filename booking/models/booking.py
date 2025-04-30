from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import localdate

from booking.choices import BookingStatusChoices


class Booking(models.Model):
    beach = models.ForeignKey(
        to='beach.Beach',
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booking_date = models.DateField()
    guest_count = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    user = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    sunbeds = models.ManyToManyField(
        to='sunbed.Sunbed',
        related_name="bookings",
        through="booking.SunbedBooking"
    )

    inventory_items = models.ManyToManyField(
        to='inventory.InventoryItem',
        related_name='bookings',
        through='booking.InventoryBooking'
    )

    booked_by = models.ForeignKey(
        to='account.User',
        on_delete=models.SET_NULL,
        related_name="booked_bookings",
        blank=True, null=True
    )

    status = models.CharField(
        max_length=10,
        choices=BookingStatusChoices.choices,
        default=BookingStatusChoices.PENDING.value
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
        # 3) guest_count ⇄ sunbeds must match, and ≥ 1
        # —————————————————————————————————————————————
        sb_count = (
            self.sunbeds.through.objects.filter(booking=self).count()
            if self.pk else
            self.sunbeds.count()
        )
        if sb_count < 1:
            raise ValidationError({'sunbeds': "At least one sunbed must be booked."})
        elif sb_count != self.guest_count:
            raise ValidationError({'guest_count': "Number of guests must match number of sunbeds booked."})

        # —————————————————————————————————————————————
        # 4) Sunbeds must belong to this beach & not already booked on this date
        # —————————————————————————————————————————————
        errors = {}
        for sb in (self.sunbeds.all() if self.pk else self.sunbeds.model.objects.filter(bookings=self)):
            if sb.beach_id != self.beach_id:
                errors.setdefault('sunbeds', []).append(
                    f"Sunbed #{sb.id} does not belong to beach “{self.beach.title}”."
                )

            conflict_qs = self.sunbeds.through.objects.filter(
                booking__status__in=['confirmed', 'pending'],
                booking__booking_date=self.booking_date,
                sunbed__in=self.sunbeds.all(),
            )
            if self.pk:
                conflict_qs = conflict_qs.exclude(booking=self)
            if conflict_qs.exists():
                errors.setdefault('sunbeds', []).append(
                    "One or more sunbeds are already booked for this date."
                )

        # —————————————————————————————————————————————
        # 5) Inventory items must belong to this beach, have qty ≥1,
        #    and not exceed available stock for that date
        # —————————————————————————————————————————————
        for ib in self.inventory_items.through.objects.filter(booking=self):
            inv = ib.inventory_item
            # a) same-beach check
            if inv.beach_id != self.beach_id:
                errors.setdefault('inventory_items', []).append(
                    f"Item “{inv.name}” is not sold on beach “{self.beach.title}”."
                )

            # b) availability check
            conflict_qs = self.inventory_items.through.objects.filter(
                inventory_item__in=self.inventory_items.all(),
                booking__status__in=['confirmed', 'pending'],
                booking__booking_date=self.booking_date,
            )
            if self.pk:
                conflict_qs = conflict_qs.exclude(booking=self)
            if conflict_qs.exists():
                errors.setdefault('inventory_items', []).append(
                    "One or more inventory items are already booked for this date."
                )

        # —————————————————————————————————————————————
        # 6) (Optional) enforce beach seasonality, e.g. within open/close dates
        # —————————————————————————————————————————————
        # if hasattr(self.beach.season, 'opening_date') and hasattr(self.beach.season, 'closing_date'):
        #     # open 9 close 5
        #     if self.beach.season.opening_date.month > self.beach.season.closing_date.month:
        #         # 9-12 1-5
        #         if (
        #                 (self.beach.season.opening_date.month < self.booking_date.month < 12) or
        #                 (self.beach.season.closing_date.month > self.booking_date.month > 1)
        #         ):
        #
        #     elif self.beach.season.opening_date.month > self.beach.season.closing_date.month:
        #         self.booking_date.month
        #     else:
        #         ( <= self.booking_date.month <= ):
        #         raise ValidationError({'booking_date': f"Must book between {self.beach.season.opening_date.strftime('%B')} and {self.beach.season.closing_date.strftime('%B')}."})

        if errors:
            raise ValidationError(errors)
