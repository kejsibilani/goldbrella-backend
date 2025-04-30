import factory

from services.models import Rule


RULES = [
    "No Littering",
    "No Smoking",
    "No Pets",
    "No Alcohol",
    "No Glass Containers",
    "No Fires",
    "No Fishing",
    "No Camping",
    "No Overnight Stays",
    "No Diving",
    "No Loud Music",
    "No Skateboarding",
    "No Bicycles",
    "No Unsupervised Children",
    "No Drones",
    "No Unauthorized Vehicles",
    "No Feeding Wildlife",
    "No Vandalism",
    "No Climbing Dunes",
    "No Ball Games",
    "No Fireworks",
    "No Barbecues",
    "No Tents",
    "No Soap",
    "No Jet Skis",
    "No Unauthorized Vending",
    "No Kites",
    "No Musical Instruments",
    "No Loudspeakers",
    "No Swimming After Dark",
    "No Motorboats",
    "No Chemicals",
    "No Hoverboards",
    "No Rollerblading",
    "No Bonfires",
    "No Climbing Rocks",
    "No Feeding Seagulls",
    "No Outside Food",
    "No Outside Beverages",
    "No Smoking Vapes",
    "No Metal Detectors",
    "No Unregistered Crafts",
    "No Kite Surfing",
    "No Unattended Belongings",
    "No Balloons",
    "No Lawn Chairs",
    "No Picnic Baskets",
    "No Hammocks",
    "No Ring Toss",
    "No Frisbees"
]

class RuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rule
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: RULES[n % len(RULES)])
