from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Lower

from booking.choices import BookingStatusChoices


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    reusable_item = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)]
    )

    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal(0))]
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

    def check_availability(self, booking_date, quantity: int, on_demand: bool, **excluded_kwargs):
        # on-demand inventory is always available
        if on_demand: return True
        # reusable inventory is checked for availability based on date and quantity
        if self.reusable_item:
            booked_inventory = self.booked_inventory.filter(
                booking__booking_date=booking_date,
                booking__status__in=[
                    BookingStatusChoices.CONFIRMED.value,
                    BookingStatusChoices.RESERVED.value
                ]
            ).exclude(**excluded_kwargs).values_list('quantity', flat=True)
            remaining_inventory = self.quantity - sum(booked_inventory)
            if remaining_inventory >= quantity:
                return True
            return False
        # non-reusable inventory is checked for availability based on quantity
        if self.quantity >= quantity:
            return True
        return False
