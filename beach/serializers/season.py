from rest_framework import serializers

from beach.models import BeachOpeningSeason


class BeachOpeningSeasonSerializer(serializers.ModelSerializer):
    start_month = serializers.SerializerMethodField()
    end_month = serializers.SerializerMethodField()

    class Meta:
        model = BeachOpeningSeason
        fields = "__all__"

    @staticmethod
    def get_start_month(instance):
        return instance.opening_date.strftime("%B")

    @staticmethod
    def get_end_month(instance):
        return instance.closing_date.strftime("%B")
