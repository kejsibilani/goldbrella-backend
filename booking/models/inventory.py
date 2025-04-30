from django.core.exceptions import ValidationError
from django.db import models


class InventoryBooking(models.Model):
    booking = models.ForeignKey(
        to='booking.Booking',
        on_delete=models.CASCADE,
        related_name="inventory_bookings"
    )
    inventory = models.ForeignKey(
        to='inventory.Inventory',
        on_delete=models.CASCADE,
        related_name="inventory_bookings"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Inventory Item Bookings"
        verbose_name = "Inventory Item Booking"

    def __str__(self):
        return f"Inventory item {self.inventory.id} booked for {self.booking.user.username}"

    def clean(self):
        # 1) Inventory must live on the same beach
        if self.inventory.beach_id != self.booking.beach_id:
            raise ValidationError("Inventory and Booking must share the same beach.")
