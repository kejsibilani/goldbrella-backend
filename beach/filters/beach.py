from django_filters.rest_framework import FilterSet, filters
from django.db.models import ImageField
from django_filters.filters import CharFilter
from beach.models import Beach
from django.db.models.functions import Lower
from django.db.models import Func, F, FloatField, ExpressionWrapper
from django.db.models.expressions import RawSQL
import unicodedata
from django.db.models import Q

class Unaccent(Func):
    function = 'unaccent'
    output_field = CharFilter().field

class BeachFilterSet(FilterSet):
    title = filters.CharFilter(method='accent_insensitive_title')
    description = filters.CharFilter(lookup_expr='icontains')
    lat = filters.NumberFilter(method='filter_proximity')
    lng = filters.NumberFilter(method='filter_proximity')
    radius = filters.NumberFilter(method='filter_proximity')
    city = filters.CharFilter(method='filter_city_or_location')
    location = filters.NumberFilter(field_name='location', lookup_expr='exact')

    class Meta:
        model = Beach
        fields = [
            "title",
            "description",
            "latitude",
            "longitude",
            "location",
            "facilities",
            "rules",
            "image",
            "created",
            "updated",
        ]
        filter_overrides = {
            ImageField: {
                'filter_class': CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
        }

    def accent_insensitive_title(self, queryset, name, value):
        # Try to use unaccent if available, else fallback to python-side normalization
        try:
            return queryset.annotate(
                title_unaccent=Unaccent(Lower('title'))
            ).filter(title_unaccent__icontains=unicodedata.normalize('NFKD', value).encode('ASCII', 'ignore').decode('utf-8').lower())
        except Exception:
            # fallback: python-side normalization
            def normalize(s):
                return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8').lower()
            return [b for b in queryset if normalize(b.title).find(normalize(value)) != -1]

    def filter_proximity(self, queryset, name, value):
        lat = self.data.get('lat')
        lng = self.data.get('lng')
        radius = self.data.get('radius', 10)  # default 10km
        if lat and lng:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
            # Haversine formula (distance in km)
            raw_sql = (
                "6371 * acos(cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)))"
            )
            return queryset.annotate(
                distance=RawSQL(raw_sql, (lat, lng, lat))
            ).filter(distance__lte=radius).order_by('distance')
        return queryset

    def filter_city_or_location(self, queryset, name, value):
        # If value is numeric, treat as location ID
        if value.isdigit():
            return queryset.filter(location_id=int(value))
        # Otherwise, treat as city name (icontains)
        return queryset.filter(location__city__icontains=value)
