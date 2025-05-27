import factory

from beach.factories.beach import BeachFactory
from beach.models import BeachImage


class BeachImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BeachImage

    beach = factory.SubFactory(BeachFactory)
    image = factory.django.ImageField(
        filename='beach.png',
        format='PNG',
        width=800,
        height=600
    )
