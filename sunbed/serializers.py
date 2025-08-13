from rest_framework import serializers

from helpers.validators import CaseInsensitiveUniqueTogetherValidator
from sunbed.models import Sunbed


class SunbedSerializer(serializers.ModelSerializer):
    # 'row' and 'column' fields are now included for visual organization
    class Meta:
        model = Sunbed
        fields = '__all__'
        read_only_fields = ('identity',)
        validators = [
            CaseInsensitiveUniqueTogetherValidator(
                queryset=Sunbed.objects.all(),
                fields=('area', 'identity', 'zone')
            )
        ]
        extra_kwargs = {
            'price': {'min_value': 0.0},
        }


class AvailableSunbedSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()
    # 'row' and 'column' fields are now included for visual organization
    class Meta:
        model = Sunbed
        fields = '__all__'

    def get_available(self, obj):
        booking_date = self.context.get('booking_date', None)

        if booking_date is None:
            return None
        elif obj.check_availability(booking_date):
            return True
        return False


class SunbedQuerySerializer(serializers.Serializer):
    only_available = serializers.BooleanField(default=False)
    booking_date = serializers.DateField(required=False)

    def validate(self, data):
        only_available = data.get("only_available")
        booking_date = data.get("booking_date")

        if only_available and not booking_date:
            raise serializers.ValidationError(
                {'detail': '`only_available` should be specified with either `booking_date`'}
            )
        return data
