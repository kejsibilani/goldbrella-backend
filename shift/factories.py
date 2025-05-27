from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from random import choice
from random import randint

import factory

from account.factories import StaffFactory
from shift.models import Shift
from zone.factories import ZoneFactory


class ShiftFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shift

    start_time = factory.LazyFunction(
        lambda: time(
            hour=randint(6, 12),
            minute=choice([0, 15, 30, 45])
        )
    )
    end_time = factory.LazyAttribute(
        lambda o: (
            (datetime.combine(date.today(), o.opening_time)
             + timedelta(hours=randint(4, 10)))
            .time()
        )
    )
    zone = factory.SubFactory(ZoneFactory)
    user = factory.SubFactory(StaffFactory)
