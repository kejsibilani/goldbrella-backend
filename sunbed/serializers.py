from rest_framework import serializers

from helpers.validators import CaseInsensitiveUniqueTogetherValidator
from sunbed.models import Sunbed


class SunbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sunbed
        fields = '__all__'
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
    guest_count = serializers.IntegerField(required=False)
    booking_date = serializers.DateField(required=False)

    @staticmethod
    def validate_guest_count(value):
        if value < 1:
            raise serializers.ValidationError({
                'guest_count': 'Guest count must be greater than or equal to 1.'
            })
        return value

    def validate(self, data):
        only_available = data.get("only_available")
        booking_date = data.get("booking_date")
        guest_count = data.get("guest_count")

        if only_available and guest_count and not booking_date:
            raise serializers.ValidationError(
                {'detail': '`only_available` and `guest_count` should be specified with `booking_date`'}
            )
        if guest_count and not only_available and not booking_date:
            raise serializers.ValidationError(
                {'detail': '`guest_count` should be specified with either `booking_date` or `booking_date` and `only_available`'}
            )
        if only_available and not guest_count and not booking_date:
            raise serializers.ValidationError(
                {'detail': '`only_available` should be specified with either `booking_date` or `booking_date` and `guest_count`'}
            )
        return data
