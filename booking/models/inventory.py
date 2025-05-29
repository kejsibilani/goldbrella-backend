from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class BookedInventory(models.Model):
    booking = models.ForeignKey(
        to='booking.Booking',
        on_delete=models.CASCADE,
        related_name="inventory"
    )

    inventory_item = models.ForeignKey(
        to='inventory.InventoryItem',
        on_delete=models.CASCADE,
        related_name="booked_inventory"
    )
    on_demand = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Inventory Item Bookings"
        verbose_name = "Inventory Item Booking"

    def __str__(self):
        return f"Inventory item {self.inventory_item.id} booked for {self.booking.user.username}"

    def clean(self):
        # 1) Inventory must live on the same beach
        if self.inventory_item.beach_id != self.booking.beach_id:
            raise ValidationError("Inventory item and Booking must share the same beach.")

        # 2) Inventory must be available
        is_available = self.inventory_item.check_availability(
            booking_date=self.booking.booking_date,
            quantity=self.quantity,
            on_demand=self.on_demand,
            pk=self.pk
        )
        if not is_available:
            raise ValidationError(f"Inventory item is not available for {self.booking.booking_date}.")
