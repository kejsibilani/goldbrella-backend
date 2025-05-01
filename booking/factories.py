from random import randint, sample

import factory
from factory import fuzzy

from account.factories import UserFactory
from beach.factories import BeachFactory
from booking.models import Booking
from inventory.factories import InventoryItemFactory
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
                bookings__status__in=['confirmed', 'pending'],
                bookings__booking_date=self.booking_date,
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
            for item in extracted:
                self.inventory_items.add(item)
            return
        # otherwise pick 1–3 available items, create more if needed
        needed = randint(1, 8)

        # find all items on this beach not already booked on this date
        available = self.inventory_items.model.objects.filter(beach=self.beach, quantity__gte=self.guest_count).exclude(
            bookings__status__in=['confirmed', 'pending'],
            bookings__booking_date=self.booking_date
        )

        # if not enough, create extras
        while available.count() <= needed:
            InventoryItemFactory(beach=self.beach, quantity=self.guest_count)

            available = self.inventory_items.model.objects.filter(
                beach=self.beach,
                quantity__gte=self.guest_count
            ).exclude(
                bookings__status__in=['confirmed', 'pending'],
                bookings__booking_date=self.booking_date
            )

        chosen = sample(list(available), needed)
        for item in chosen:
            inv_item = self.inventory_items.through.objects.filter(
                inventory_item=item,
                booking=self
            ).first()
            if inv_item:
                inv_item.inventory_quantity = self.guest_count
                inv_item.save()
            else:
                self.inventory_items.add(
                    item,
                    through_defaults={'inventory_quantity': self.guest_count}
                )
