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

BAR_PRODUCTS = [
    # Cocktails
    ("Cocktail Paradise", "Cocktails", 12.50),
    ("Mojito Classic", "Cocktails", 11.00),
    ("Pina Colada", "Cocktails", 13.00),
    # Beer
    ("Beach Beer", "Beer", 6.00),
    ("Premium Lager", "Beer", 7.50),
    # Wine
    ("Sunset Wine", "Wine", 8.00),
    ("Sparkling Wine", "Wine", 10.00),
    # Non-Alcoholic
    ("Fresh Coconut", "Non-Alcoholic", 4.50),
    ("Fruit Smoothie", "Non-Alcoholic", 7.50),
    ("Iced Coffee", "Non-Alcoholic", 5.50),
    # Food
    ("Beach Burger", "Food", 15.00),
    ("Fish Tacos", "Food", 13.50),
    ("Caesar Salad", "Food", 11.00),
    ("Nachos Supreme", "Food", 9.50),
]

class InventoryItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InventoryItem
        django_get_or_create = ('name', 'beach',)

    name = fuzzy.FuzzyChoice(INVENTORY_LIST)
    price = fuzzy.FuzzyDecimal(50.0, 500.0, precision=2)
    reusable_item = factory.Faker('boolean')
    quantity = fuzzy.FuzzyInteger(1, 100)
    beach = factory.SubFactory(BeachFactory)
    category = "Other"

class BarProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InventoryItem
        django_get_or_create = ('name', 'beach',)

    name = factory.LazyAttribute(lambda o: o.product[0])
    category = factory.LazyAttribute(lambda o: o.product[1])
    price = factory.LazyAttribute(lambda o: o.product[2])
    reusable_item = False
    quantity = 100
    beach = factory.SubFactory(BeachFactory)
    product = fuzzy.FuzzyChoice(BAR_PRODUCTS)

    class Params:
        product = factory.Trait()
