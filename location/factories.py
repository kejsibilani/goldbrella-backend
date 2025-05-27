import factory

from location.models import Location


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location
        django_get_or_create = ('country', 'city',)

    # country_names is a dict of code→name; choices are keys
    country = factory.Faker("country_code")
    city = factory.Faker('city')
