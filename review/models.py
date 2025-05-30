from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from account.views import users


# Create your models here.
class Review(models.Model):
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    booking = models.OneToOneField(
        to='booking.Booking',
        on_delete=models.CASCADE,
        related_name='review'
    )
    user = models.ForeignKey(
        to='users.User',
        on_delete=models.SET_NULL,
        related_name='reviews',
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Reviews'
        verbose_name = 'Review'

    def __str__(self):
        return str(self.rating)
