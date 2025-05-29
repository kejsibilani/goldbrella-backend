from random import randint, sample

import factory
from factory import fuzzy
from factory import post_generation

from account.factories import UserFactory
from beach.factories import BeachFactory
from booking.choices import BookingStatusChoices
from booking.factories.inventory import BookedInventoryFactory
from booking.models import Booking
from inventory.factories import InventoryItemFactory
from sunbed.factories import SunbedFactory


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    beach = factory.SubFactory(BeachFactory)
    booking_date = factory.Faker('date_between', start_date='today', end_date='+30d')
    guest_count = fuzzy.FuzzyInteger(1, 8)
    user = factory.SubFactory(UserFactory)
    booked_by = factory.SubFactory(UserFactory)

    @post_generation
    def sunbeds(self, create, extracted, **kwargs):
        """
        1) ensure guest_count == number of sunbeds
        2) sunbeds belong to the same beach
        3) sunbeds aren’t double‐booked on booking_date
        """
        if not create:
            return

        # if the test explicitly passed a list of sunbed instances:
        if extracted:
            for sb in extracted:
                self.sunbeds.add(sb)
            return

        needed = self.guest_count

        # find all sunbeds on this beach not already booked/reserved on this date
        qs = self.sunbeds.model.objects.filter(beach=self.beach).exclude(
            bookings__booking_date=self.booking_date,
            bookings__status__in=[
                BookingStatusChoices.RESERVED.value,
                BookingStatusChoices.CONFIRMED.value,
            ],
        )
        available = list(qs)

        # if not enough, create extra sunbeds on the same beach
        while len(available) < needed:
            new_sb = SunbedFactory(beach=self.beach)
            available.append(new_sb)

        chosen = sample(available, needed)
        for sb in chosen:
            # this will create the through‐model entry SunbedBooking
            self.sunbeds.add(sb)

    @post_generation
    def inventory(self, create, extracted, **kwargs):
        """
        1) inventory items live on the same beach
        2) inventory items have enough quantity
        3) quantity booked == guest_count (or on_demand overrides)
        """
        if not create:
            return

        # if the test explicitly passed inventory_item instances:
        if extracted:
            for inv_item in extracted:
                BookedInventoryFactory(
                    booking=self,
                    inventory_item=inv_item,
                    quantity=self.guest_count,
                    on_demand=False
                )
            return

        # otherwise pick between 1 and guest_count distinct items
        needed = randint(1, self.guest_count)
        InventoryItem = InventoryItemFactory._meta.model

        # find all items on this beach with enough quantity and not booked already
        qs = InventoryItem.objects.filter(beach=self.beach, quantity__gte=self.guest_count).exclude(
            booked_inventory__booking__booking_date=self.booking_date,
            booked_inventory__booking__status__in=[
                BookingStatusChoices.RESERVED.value,
                BookingStatusChoices.CONFIRMED.value,
            ],
        )
        available = list(qs)

        # if not enough, create more
        while len(available) < needed:
            new_item = InventoryItemFactory(beach=self.beach, quantity=self.guest_count)
            available.append(new_item)

        chosen = sample(available, needed)
        for item in chosen:
            BookedInventoryFactory(
                booking=self,
                inventory_item=item,
                quantity=self.guest_count,
                on_demand=False
            )
