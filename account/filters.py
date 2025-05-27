from django_filters.rest_framework import FilterSet, filters

from account.choices import UserRoleChoices
from account.models import User


class UserFilterSet(FilterSet):
    email = filters.CharFilter(lookup_expr='icontains')
    phone_number = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    preferred_language = filters.CharFilter(lookup_expr='icontains')
    role = filters.MultipleChoiceFilter(choices=UserRoleChoices.values)
    date_joined = filters.DateTimeFromToRangeFilter()
    is_superuser = filters.BooleanFilter()
    is_active = filters.BooleanFilter()

    class Meta:
        model = User
        fields = '__all__'
