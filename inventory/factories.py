import factory
from factory import fuzzy

from beach.factories import BeachFactory
from inventory.models import InventoryItem


INVENTORY_LIST = [
    "Umbrella Rental",
    "Towel Rental",
    "Beach Chair Rental",
    "Cabana Rental",
    "Snorkel Gear Rental",
    "Kayak Rental",
    "Paddleboard Rental",
    "Surfboard Rental",
    "Jet Ski Rental",
    "Boat Tours",
    "Fishing Charter",
    "Parasailing",
    "Scuba Diving Lessons",
    "Surf Lessons",
    "Sailing Lessons",
    "Windsurf Lessons",
    "Stand-Up Paddle Lessons",
    "Beach Yoga Classes",
    "Beach Fitness Classes",
    "Massage",
    "Beach Picnic Package",
    "Barbecue Package",
    "Sunset Cruise",
    "Dolphin Watching Tour",
    "Snorkel Tours",
    "Sunscreen Sales",
    "Beach Photography",
    "Professional Photoshoots",
    "Drone Footage",
    "Beach Bonfire Setup",
    "Fireworks Display",
    "Beach Party Package",
    "Event Planning",
    "Catering Service",
    "Hammock Rental",
    "Bicycle Rental",
    "Electric Scooter Rental",
    "Beach Umbrella Sale",
    "Artisan Craft Stalls",
    "Ice Cream Delivery",
    "Snack Delivery",
    "Water Delivery",
    "Premium Parking",
    "VIP Access",
    "Fast-Track Entry",
    "Guided Nature Walks",
    "Birthday Packages",
    "Wedding Ceremony",
    "Corporate Events",
    "Kite Surf Lessons"
]

class InventoryItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InventoryItem
        django_get_or_create = ('name', 'beach',)

    name = fuzzy.FuzzyChoice(INVENTORY_LIST)
    price = fuzzy.FuzzyDecimal(50.0, 500.0, precision=2)
    discount_percentage = fuzzy.FuzzyDecimal(0.0, 100.0, precision=2)
    quantity = fuzzy.FuzzyInteger(1, 100)
    beach = factory.SubFactory(BeachFactory)
