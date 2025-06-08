from django.db import models


class ScheduledEmailStatusChoices(models.TextChoices):
    SCHEDULED = ('scheduled', 'Scheduled')
    FAILED = ('failed', 'Failed')
    SENT = ('sent', 'Sent')
