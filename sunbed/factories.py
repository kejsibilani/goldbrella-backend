import factory
from factory import fuzzy

from beach.factories import BeachFactory
from sunbed.choices import SunbedTypeChoices
from sunbed.models import Sunbed


AREAS = ['A', 'B']

class SunbedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sunbed
        django_get_or_create = ('area', 'identity', 'beach',)

    area = factory.Sequence(lambda n: AREAS[n % len(AREAS)])
    identity = factory.Sequence(
        lambda n: f"{AREAS[n % len(AREAS)]}{(n // len(AREAS)) + 1}"
    )
    price = fuzzy.FuzzyDecimal(50.0, 5000.0, precision=2)
    discount_percentage = fuzzy.FuzzyDecimal(0.0, 100.0, precision=2)
    sunbed_type = fuzzy.FuzzyChoice(SunbedTypeChoices.values)
    beach = factory.SubFactory(BeachFactory)
