import factory
from factory import fuzzy

from booking.factories import BookingFactory
from payment.choices import PaymentMethodChoices, PaymentStatusChoices
from payment.models import BookingPayment


class BookingPaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookingPayment
        django_get_or_create = ('booking', 'transaction_id')

    transaction_id = factory.Faker('uuid4')
    payment_method = fuzzy.FuzzyChoice(PaymentMethodChoices.values)
    payment_status = fuzzy.FuzzyChoice(PaymentStatusChoices.values)
    paid_amount = fuzzy.FuzzyDecimal(0, 100)
    booking = factory.SubFactory(BookingFactory)
