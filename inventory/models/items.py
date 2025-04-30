from uuid import uuid4

from django.db import models


class InventoryItem(models.Model):
    identity = models.CharField(max_length=100, default=uuid4)
    inventory = models.ForeignKey(
        to='inventory.Inventory',
        on_delete=models.CASCADE,
        related_name='items'
    )

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
