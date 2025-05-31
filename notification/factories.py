import factory
from factory import fuzzy

from account.factories import UserFactory
from notification.models import Notification


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    message = factory.Faker('sentence')
    is_read = fuzzy.FuzzyChoice([True, False])
    user = factory.SubFactory(UserFactory)
