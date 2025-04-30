from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from services.models import Facility


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'
        extra_kwargs = {
            'name': {
                'validators': [
                    UniqueValidator(queryset=Facility.objects.all(), lookup='iexact')
                ]
            }
        }
