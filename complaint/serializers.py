from rest_framework import serializers

from complaint.models import Complaint
from helpers.fkeys.contenttype import ContentTypePrimaryKeyRelatedField


class ComplaintSerializer(serializers.ModelSerializer):
    related_content_type = ContentTypePrimaryKeyRelatedField(required=False)

    class Meta:
        model = Complaint
        fields = '__all__'
