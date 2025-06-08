from rest_framework import serializers

from mailer.models import ScheduledEmail


class ScheduledEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledEmail
        exclude = ('subject', 'content', 'system_generated')
