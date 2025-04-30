import factory

from services.models import Facility


FACILITIES = [
    "Restrooms",
    "Outdoor Showers",
    "Changing Rooms",
    "Lifeguard Stations",
    "Lifeguard Towers",
    "First Aid Stations",
    "AED Stations",
    "Trash Bins",
    "Recycling Bins",
    "Beach Umbrellas",
    "Sun Loungers",
    "Picnic Tables",
    "BBQ Grills",
    "Parking Lot",
    "Parking Meters",
    "Boardwalk",
    "Beach Shuttle Stops",
    "Bike Racks",
    "Information Kiosks",
    "Lost and Found",
    "Beach Café",
    "Snack Bar",
    "Water Fountains",
    "Foot Wash Stations",
    "Baby Changing Rooms",
    "Dog Wash Stations",
    "Playgrounds",
    "Sand Play Areas",
    "Volleyball Courts",
    "Soccer Fields",
    "Shaded Pavilions",
    "Picnic Shelters",
    "Observation Decks",
    "Beach Stage",
    "Water Sports Center",
    "Kayak Launch",
    "Boat Dock",
    "Surfboard Racks",
    "Sandcastle Areas",
    "Nature Trails",
    "Wildlife Blinds",
    "Eco Education Center",
    "Weather Stations",
    "Tide Indicators",
    "Emergency Call Boxes",
    "Fish Cleaning Stations",
    "Accessibility Ramps",
    "Meditation Zones",
    "Beach Huts",
    "Visitor Center"
]

class FacilityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Facility
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: FACILITIES[n % len(FACILITIES)])
