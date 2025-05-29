import factory
from factory.fuzzy import FuzzyInteger

from booking.models import BookedInventory
from inventory.factories import InventoryItemFactory

class BookedInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookedInventory

    # In most cases you'll pass `booking=` explicitly (e.g. from your BookingFactory hook),
    # but if you don't, this will create one—and avoid infinite recursion by disabling
    # the related inventory-generation hook there.
    booking = factory.SubFactory(
        'booking.factories.BookingFactory',
        sunbeds=[],         # disable sunbeds hook
        inventory=[]        # disable inventory hook
    )

    inventory_item = factory.SubFactory(InventoryItemFactory)
    quantity = FuzzyInteger(1, 8)
    on_demand = False
