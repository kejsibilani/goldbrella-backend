from rest_framework import serializers

from helpers.fkeys.booking import BookingPrimaryKeyRelatedField
from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    booking = BookingPrimaryKeyRelatedField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user',)
