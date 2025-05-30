from django.db import models


class ComplaintStatusChoices(models.TextChoices):
    REGISTERED = ('registered', 'Registered')
    PROCESSING = ('processing', 'Processing')
    CANCELLED = ('cancelled', 'Cancelled')
    RESOLVED = ('resolved', 'Resolved')
