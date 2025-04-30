from random import randint, sample, choice

import factory

from beach.factories.location import BeachLocationFactory
from beach.models import Beach
from services.factories import FacilityFactory, RuleFactory
from services.factories.facility import FACILITIES
from services.factories.rule import RULES


class BeachFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Beach
        django_get_or_create = ("location", "longitude", "latitude",)

    description = factory.Faker('paragraph', nb_sentences=3)
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    location = factory.SubFactory(BeachLocationFactory)

    # keep track per-location how many titles we've generated
    _title_counters = {}
    # meaningful suffixes to rotate through
    _suffixes = [
        "Cove", "Sands", "Bay", "Lagoon",
        "Pier", "Point", "Shore", "Vista",
        "Grove", "Heights"
    ]

    @factory.lazy_attribute
    def title(self):
        loc = self.location
        if loc.pk is None:
            loc.save()

        # bump the count for this location
        count = BeachFactory._title_counters.get(loc.pk, 0) + 1
        BeachFactory._title_counters[loc.pk] = count

        base = f"{loc.city} Beach"
        if count == 1:
            return base

        # pick the (count-2)th suffix in the list, wrapping around
        suffix = choice(BeachFactory._suffixes)
        return f"{loc.city} {suffix}"

    @factory.post_generation
    def facilities(self, create, extracted, **kwargs):
        if not create:
            return
        chosen = extracted or sample(FACILITIES, randint(1, 3))
        for name in chosen:
            self.facilities.add(FacilityFactory(name=name))

    @factory.post_generation
    def rules(self, create, extracted, **kwargs):
        if not create:
            return
        chosen = extracted or sample(RULES, randint(1, 3))
        for name in chosen:
            self.rules.add(RuleFactory(name=name))
