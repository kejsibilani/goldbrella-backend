from django.db import models
from django.utils import timezone

from mailer.choices import ScheduledEmailStatusChoices


# Create your models here.
class ScheduledEmail(models.Model):
    subject = models.TextField()
    content = models.TextField()

    receivers = models.JSONField(default=list)
    sender = models.JSONField(default=list)

    system_generated = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        default=ScheduledEmailStatusChoices.SCHEDULED.value,
        choices=ScheduledEmailStatusChoices.choices,
        max_length=15
    )

    class Meta:
        verbose_name_plural = "Scheduled Emails"
        verbose_name = "Scheduled Email"
