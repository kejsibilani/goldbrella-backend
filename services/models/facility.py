from django.db import models
from django.db.models.functions import Lower


class Facility(models.Model):
    name = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Facilities"
        verbose_name = "Facility"
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='unique_facilities'
            ),
        ]

    def __str__(self):
        return self.name
