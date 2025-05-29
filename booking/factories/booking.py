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
    user = factory.SubFactory(UserFactory)
    booked_by = factory.SubFactory(UserFactory)

    @post_generation
    def sunbeds(self, create, extracted, **kwargs):
        """
        1) sunbeds belong to the same beach
        2) sunbeds aren’t double‐booked on booking_date
        """
        if not create:
            return

        # if the test explicitly passed a list of sunbed instances:
        if extracted:
            for sb in extracted:
                self.sunbeds.add(sb)
            return

        needed = randint(1, 3)

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

    @factory.post_generation
    def inventory(self, create, extracted, **kwargs):
        """
        Book inventory items so that:
          - quantity = number of sunbeds on this booking,
          - if you passed explicit inventory_item instances, each gets that quantity,
          - otherwise pick between 1 and that quantity of distinct items.
        """
        if not create:
            return

        # how many seats we actually have:
        booked_count = self.sunbeds.count()

        # if test passed inventory_item instances, use those
        if extracted:
            for inv_item in extracted:
                BookedInventoryFactory(
                    booking=self,
                    inventory_item=inv_item,
                    quantity=booked_count,
                    on_demand=False
                )
            return

        # otherwise pick a random number of distinct items
        needed = randint(1, booked_count)
        InventoryItemModel = InventoryItemFactory._meta.model

        qs = InventoryItemModel.objects.filter(
            beach=self.beach,
            quantity__gte=booked_count
        ).exclude(
            booked_inventory__booking__booking_date=self.booking_date,
            booked_inventory__booking__status__in=[
                BookingStatusChoices.RESERVED.value,
                BookingStatusChoices.CONFIRMED.value,
            ],
        )
        available = list(qs)

        while len(available) < needed:
            available.append(
                InventoryItemFactory(beach=self.beach, quantity=booked_count)
            )

        for item in sample(available, needed):
            BookedInventoryFactory(
                booking=self,
                inventory_item=item,
                quantity=booked_count,
                on_demand=False
            )
