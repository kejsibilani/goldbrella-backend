import factory

from beach.factories.beach import BeachFactory
from beach.models import BeachImage


class BeachImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BeachImage
        django_get_or_create = ('beach', 'link',)

    beach = factory.SubFactory(BeachFactory)
    link = factory.Faker('image_url')
