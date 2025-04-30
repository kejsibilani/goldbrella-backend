import factory

from beach.models import BeachLocation


class BeachLocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BeachLocation
        django_get_or_create = ('country', 'city',)

    # country_names is a dict of code→name; choices are keys
    country = factory.Faker("country_code")
    city = factory.Faker('city')
