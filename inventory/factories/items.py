from random import randint

import factory
from factory import fuzzy

from inventory.factories.inventory import InventoryFactory
from inventory.models import InventoryItem


class InventoryItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InventoryItem
        django_get_or_create = ('inventory', 'identity',)

    identity = factory.Sequence(lambda n: f"{n+1}{randint(100, 999)}")
    inventory = factory.SubFactory(InventoryFactory)
