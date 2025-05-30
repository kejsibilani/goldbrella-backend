from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from complaint.choices import ComplaintStatusChoices


# Create your models here.
class Complaint(models.Model):
    creator = models.ForeignKey(
        to='account.User',
        on_delete=models.SET_NULL,
        related_name='complaints',
        null=True
    )

    details = models.TextField()
    status = models.CharField(
        default=ComplaintStatusChoices.REGISTERED.value,
        choices=ComplaintStatusChoices.choices,
        max_length=20
    )

    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    related_content_type = models.ForeignKey(
        to='contenttypes.ContentType',
        on_delete=models.CASCADE,
        related_name='complaints',
        blank=True, null=True
    )
    related_object = GenericForeignKey('related_content_type', 'related_object_id')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Complaints'
        verbose_name = 'Complaint'


    def __str__(self):
        return str(self.creator)
