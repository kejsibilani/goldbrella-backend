from django.utils.translation import gettext_lazy as _

from rest_framework.validators import UniqueTogetherValidator, qs_filter


class CaseInsensitiveUniqueTogetherValidator(UniqueTogetherValidator):
    message = _('The case insensitive fields {field_names} must make a unique set.')

    def filter_queryset(self, attrs, queryset, serializer):
        """
        Filter the queryset to all instances matching the given attributes.
        """
        # field names => field sources
        sources = [
            serializer.fields[field_name].source
            for field_name in self.fields
        ]

        # If this is an update, then any unprovided field should
        # have it's value set based on the existing instance attribute.
        if serializer.instance is not None:
            for source in sources:
                if source not in attrs:
                    attrs[source] = getattr(serializer.instance, source)

        # Determine the filter keyword arguments and filter the queryset.
        filter_kwargs = {}
        for source in sources:
            if hasattr(serializer.fields[source], 'queryset'):
                filter_kwargs[source] = attrs[source]
            else:
                filter_kwargs[source + '__iexact'] = attrs[source]
        return qs_filter(queryset, **filter_kwargs)
