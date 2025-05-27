from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from random import choice
from random import randint

import factory

from beach.choices import OpeningDayChoices
from beach.factories.season import BeachOpeningSeasonFactory
from beach.models import BeachOpeningHour


class BeachOpeningHourFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BeachOpeningHour
        django_get_or_create = ('season', 'day',)

    season = factory.SubFactory(BeachOpeningSeasonFactory)
    weekday = factory.Iterator([c for c in OpeningDayChoices.values])
    opening_time = factory.LazyFunction(
        lambda: time(
            hour=randint(6, 12),
            minute=choice([0, 15, 30, 45])
        )
    )
    closing_time = factory.LazyAttribute(
        lambda o: (
            (datetime.combine(date.today(), o.opening_time)
             + timedelta(hours=randint(4, 10)))
            .time()
        )
    )
