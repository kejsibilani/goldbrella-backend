from uuid import uuid4

from django.db import models


class InventoryItem(models.Model):
    identity = models.CharField(max_length=100, default=uuid4)
    inventory = models.ForeignKey(
        to='inventory.Inventory',
        on_delete=models.CASCADE,
        related_name='items'
    )

    def is_booked(self, booking_date):
        """
        Checks if a given booking date is already booked in the inventory.

        :param booking_date: The date to check for existing bookings.
        :type booking_date: datetime.date
        :return: True if the item is booked for booking date, False otherwise.
        :rtype: bool
        """
        return self.inventory_bookings.filter(
            booking__booking_date=booking_date
        ).exists()

    class Meta:
        verbose_name_plural = "Inventory Items"
        verbose_name = "Inventory Item"
        constraints = [
            models.UniqueConstraint(
                fields=['inventory', 'identity'],
                name='unique_inventory_item'
            )
        ]

    def __str__(self):
        return self.inventory.name
