from django_filters.rest_framework import FilterSet, filters

from account.models import User


class UserFilterSet(FilterSet):
    email = filters.CharFilter(lookup_expr='icontains')
    phone_number = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    preferred_language = filters.CharFilter(lookup_expr='icontains')
    assigned_area = filters.CharFilter(lookup_expr='icontains')
    department = filters.CharFilter(lookup_expr='icontains')
    office_contact = filters.CharFilter(lookup_expr='icontains')
    date_joined = filters.DateTimeFromToRangeFilter()
    is_superuser = filters.BooleanFilter()
    is_active = filters.BooleanFilter()
    is_staff = filters.BooleanFilter()

    class Meta:
        model = User
        fields = '__all__'
