from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Lower


class Inventory(models.Model):
    name = models.CharField(max_length=100)
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

    @property
    def quantity(self):
        return self.items.count()

    class Meta:
        verbose_name_plural = "Inventory Lists"
        verbose_name = "Inventory List"
        constraints = [
            models.UniqueConstraint(
                Lower('name'), 'beach',
                name='unique_inventory_item_per_beach'
            ),
        ]

    def __str__(self):
        return f"{self.beach.title} | {self.name}, {self.quantity}"
