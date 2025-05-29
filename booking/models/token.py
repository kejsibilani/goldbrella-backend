import binascii
import os

from django.db import models


class BookingToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(max_length=128, primary_key=True)
    booking = models.OneToOneField(
        to='booking.Booking',
        on_delete=models.CASCADE,
        related_name='token'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Booking Tokens"
        verbose_name = "Booking Token"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(64)).decode()

    def __str__(self):
        return self.key
