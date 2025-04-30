from decimal import Decimal
from uuid import uuid4

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Lower, Upper


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    identity = models.CharField(max_length=100, blank=True, default=uuid4)

    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal(0))]
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        validators=[
            MinValueValidator(Decimal(0)),
            MaxValueValidator(Decimal(100))
        ]
    )

    beach = models.ForeignKey(
        to='beach.Beach',
        on_delete=models.CASCADE,
        related_name="inventories"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Inventory Items"
        verbose_name = "Inventory Item"
        constraints = [
            models.UniqueConstraint(
                Lower('name'), Upper('identity'), 'beach',
                name='unique_inventory_item_per_beach'
            ),
        ]

    def __str__(self):
        return f"{self.beach.title} | {self.name}"

    def check_booking(self, booking_date):
        """
        Determine if a booking exists for the provided date.

        This method checks whether a booking has been made for the given
        date and returns a boolean result indicating the booking status.

        :param booking_date: The date for which the booking status is to be checked.
        :type booking_date: datetime.date
        :return: True if a booking exists for the given date, False otherwise.
        :rtype: bool
        """

        return self.inventory_bookings.filter(
            booking__status__in=['confirmed', 'pending'],
            booking__booking_date=booking_date
        ).exists()
