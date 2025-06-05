import factory

from beach.factories.beach import BeachFactory
from beach.models import BeachOpeningSeason


class BeachOpeningSeasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BeachOpeningSeason
        django_get_or_create = ('beach', 'opening_date', 'closing_date')

    beach = factory.SubFactory(BeachFactory)
    title = factory.Sequence(lambda n: f"Season {n}")
    opening_date = factory.Faker('date_between', start_date='-6m', end_date='-3m')
    closing_date = factory.Faker('date_between', start_date='+3m', end_date='+6m')
