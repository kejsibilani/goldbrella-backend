from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Upper

from sunbed.choices import SunbedTypeChoices


# Sunbed Model
class Sunbed(models.Model):
    sunbed_type = models.CharField(
        max_length=10,
        choices=SunbedTypeChoices.choices,
        default=SunbedTypeChoices.STANDARD.value
    )
    area = models.CharField(max_length=20)
    identity = models.CharField(max_length=5)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[
            MinValueValidator(Decimal(0)),
        ],
    )  # Added price field

    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal(0),
        validators=[
            MinValueValidator(Decimal(0)),
            MaxValueValidator(Decimal(100))
        ]
    )

    beach = models.ForeignKey(
        to='beach.Beach',
        on_delete=models.CASCADE,
        related_name="sunbeds"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Sunbeds"
        verbose_name = "Sunbed"
        constraints = [
            models.UniqueConstraint(
                Upper('area'), Upper('identity'), 'beach',
                name='unique_sunbed_per_beach'
            ),
        ]

    def __str__(self):
        return f"Sunbed {self.id} - {self.beach.title} "

    def check_availability(self, booking_date):
        """
        Checks the availability of sunbeds for a given booking date.

        If there are any existing bookings for the specified booking
        date, it returns False. Otherwise, it returns True.

        Args:
            booking_date (datetime.date): The date for which the sunbed
            availability needs to be checked.

        Returns:
            bool: True if sunbed is available for the specified date,
            otherwise False.
        """
        return not self.sunbed_bookings.filter(
            booking__status__in=['confirmed', 'pending'],
            booking__booking_date=booking_date
        ).exists()
