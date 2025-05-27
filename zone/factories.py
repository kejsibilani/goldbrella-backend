import factory
from factory import fuzzy

from account.factories import SupervisorFactory
from beach.factories import BeachFactory
from zone.choices import ZoneLocationChoices
from zone.models import Zone


class ZoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Zone
        django_get_or_create = ('location', 'beach',)

    location = fuzzy.FuzzyChoice(ZoneLocationChoices.values)
    supervisor = factory.SubFactory(SupervisorFactory)
    beach = factory.SubFactory(BeachFactory)
