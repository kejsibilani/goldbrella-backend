import factory

from beach.factories.beach import BeachFactory
from beach.models import BeachOpeningSeason


class BeachOpeningSeasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BeachOpeningSeason

    beach = factory.SubFactory(BeachFactory)
    opening_date = factory.Faker('date_between', start_date='-6m', end_date='-3m')
    closing_date = factory.Faker('date_between', start_date='+3m', end_date='+6m')
