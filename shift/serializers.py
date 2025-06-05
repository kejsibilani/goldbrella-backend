from rest_framework import serializers

from shift.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = "__all__"
        read_only_fields = ('user',)
