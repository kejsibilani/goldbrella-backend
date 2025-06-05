import factory
from factory import fuzzy

from sunbed.choices import SunbedStatusChoices
from sunbed.choices import SunbedTypeChoices
from sunbed.models import Sunbed
from zone.factories import ZoneFactory

AREAS = ['A', 'B']

class SunbedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sunbed
        django_get_or_create = ('area', 'identity', 'zone',)

    area = factory.Sequence(lambda n: AREAS[n % len(AREAS)])
    price = fuzzy.FuzzyDecimal(50.0, 5000.0, precision=2)
    sunbed_type = fuzzy.FuzzyChoice(SunbedTypeChoices.values)
    status = fuzzy.FuzzyChoice(SunbedStatusChoices.values)
    zone = factory.SubFactory(ZoneFactory)
