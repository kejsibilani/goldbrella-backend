from random import randint, sample

import factory
from factory import fuzzy

from account.factories import UserFactory
from beach.factories import BeachFactory
from booking.models import Booking
from inventory.factories import InventoryFactory
from sunbed.factories import SunbedFactory


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    beach = factory.SubFactory(BeachFactory)
    booking_date = factory.Faker('date_between', start_date='-30d', end_date='+30d')
    guest_count = fuzzy.FuzzyInteger(1, 8)
    user = factory.SubFactory(UserFactory)
    booked_by = factory.SubFactory(UserFactory)

    @factory.post_generation
    def sunbeds(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for sb in extracted:
                self.sunbeds.add(sb)
                return
        # otherwise pick 1–3 available sunbeds, create more if needed
        needed = self.guest_count

        # find all sunbeds on this beach not already booked on this date
        available = list(
            self.sunbeds.model.objects.filter(beach=self.beach).exclude(
                bookings__booking_date=self.booking_date
            )
        )

        # if not enough, create extras
        while len(available) < needed:
            available.append(SunbedFactory(beach=self.beach))

        chosen = sample(available, needed)
        for sb in chosen:
            self.sunbeds.add(sb)

    @factory.post_generation
    def inventory_items(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for sb in extracted:
                self.inventory_items.add(sb)
                return
        # otherwise pick 1–3 available sunbeds, create more if needed
        needed = randint(1, 3)

        # find all sunbeds on this beach not already booked on this date
        from django.db.models import Q

        available = self.inventory_items.model.objects.filter(beach=self.beach).filter(
            Q(
                bookings__booking_date=self.booking_date,
                quantity__gte=needed,
                _connector=Q.AND
            )
        )

        if not available:
            available = InventoryFactory.create_batch(10, beach=self.beach, quantity=randint(needed + 5, needed * 10))

        for item in available:
            self.inventory_items.add(item)
            # self.inventory_items.model.objects.filter(
            #     pk=item.pk
            # ).update(quantity=(item.quantity - needed))
