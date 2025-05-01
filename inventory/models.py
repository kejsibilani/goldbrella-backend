from decimal import Decimal
from uuid import uuid4

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Lower, Upper


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

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
        related_name="inventory_items"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Inventory Items"
        verbose_name = "Inventory Item"
        constraints = [
            models.UniqueConstraint(
                Lower('name'), 'beach',
                name='unique_inventory_item_per_beach'
            ),
        ]

    def __str__(self):
        return f"{self.beach.title} | {self.name}"

    def get_available(self, booking_date):
        """
        Calculate the available inventory for a given booking date.

        This method determines the total quantity of inventory currently
        booked with the specified booking date and subtracts it from the
        total quantity available. It accounts for bookings with statuses
        of 'confirmed' and 'pending'. If no inventory is booked, the
        entire available quantity is returned.

        :param booking_date: The date for which the available inventory is to
            be calculated.
            Type: datetime.date
        :return: The remaining quantity of inventory available for the given
            booking date. If no inventory is booked, returns the total
            available quantity.
            Type: int
        """

        booked = self.inventory_bookings.filter(
            booking__status__in=['confirmed', 'pending'],
            booking__booking_date=booking_date,
        ).aggregate(sum=models.Sum('inventory_item__quantity')).get('sum', 0) or 0
        return (self.quantity - booked) or 0

    def check_available(self, booking_date, needed: int = 1):
        """
        Checks inventory availability for a specified booking date and required
        quantity. This function evaluates the outstanding booked quantities
        for the given date and determines if the remaining inventory can fulfill
        the requested `needed` quantity.

        This function assumes that inventory bookings are stored and can
        be filtered based on booking status and date, and that the sum
        of booked inventory quantities can be successfully aggregated.

        :param booking_date: The date for which the availability needs to be checked.
        :type booking_date: datetime.date or compatible type
        :param needed: Number of units required for booking. Defaults to 1.
        :return: Whether the requested number of units (`needed`) is available.
        :rtype: bool
        """

        booked = self.inventory_bookings.filter(
            booking__status__in=['confirmed', 'pending'],
            booking__booking_date=booking_date,
        ).aggregate(sum=models.Sum('inventory__quantity')).get('sum', 0) or 0
        return (self.quantity - booked) >= needed
