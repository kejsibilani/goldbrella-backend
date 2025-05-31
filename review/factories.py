import factory

from account.factories import UserFactory
from booking.factories import BookingFactory
from review.models import Review


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    message = factory.Faker('paragraph', nb_sentences=3)
    rating = factory.Faker('random_int', min=1, max=5)
    booking = factory.SubFactory(BookingFactory)
    user = factory.SubFactory(UserFactory)
