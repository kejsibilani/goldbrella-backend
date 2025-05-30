from django.db import models


# Create your models here.
class Notification(models.Model):
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    user = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name='notifications',
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Notifications'
        verbose_name = 'Notification'
        ordering = ['-created']

    def __str__(self):
        return self.message
