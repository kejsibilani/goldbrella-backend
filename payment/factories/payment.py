import factory
from factory import fuzzy

from payment.choices import PaymentMethodChoices
from payment.choices import PaymentStatusChoices
from payment.models import BookingPayment


class BookingPaymentFactory(factory.django.DjangoModelFactory):
    """
    Factory for BookingPayment
    """
    class Meta:
        model = BookingPayment

    # Link to an invoice — assumes you have invoice/factories.py with BookingInvoiceFactory
    invoice = factory.SubFactory('invoice.factories.BookingInvoiceFactory')

    # Core payment fields
    note = factory.Faker('sentence', nb_words=8)
    amount = factory.LazyAttribute(lambda o: o.invoice.total_amount)
    payment_method = fuzzy.FuzzyChoice(PaymentMethodChoices.values)
    status = PaymentStatusChoices.INITIATED.value

    # Billing details
    billing_first_name = factory.Faker('first_name')
    billing_last_name = factory.Faker('last_name')
    billing_email = factory.Faker('email')
    billing_phone_number = factory.Faker('phone_number')

    billing_address_1 = factory.Faker('street_address')
    billing_address_2 = factory.Faker('secondary_address')
    billing_city = factory.Faker('city')
    billing_postcode = factory.Faker('postcode')
    billing_country_code = factory.LazyAttribute(lambda _: 'US')

    # Stripe / external fields
    external_intent = factory.Sequence(lambda n: f"pi_{n:08d}")
    client_secret = factory.LazyAttribute(lambda o: f"{o.external_intent}_secret")

    # Timestamps will be auto‐set by Django
