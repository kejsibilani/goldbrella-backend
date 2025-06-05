from decimal import Decimal

import factory

from booking.factories import BookingFactory
from payment.models import BookingPayment


class BookingPaymentFactory(factory.django.DjangoModelFactory):
    """
    Factory for BookingPayment (subclass of BasePayment).
    Provides reasonable defaults for BasePayment fields:
      - variant (a key in PAYMENT_VARIANTS)
      - description, total, tax, currency, delivery
      - billing_* fields, customer_ip_address.
    """
    class Meta:
        model = BookingPayment

    # Associate with a booking via a subfactory (you must have a BookingFactory)
    booking = factory.SubFactory(BookingFactory)

    # Required fields inherited from BasePayment (per django-payments usage):
    variant = factory.LazyAttribute(lambda _: 'dummy')
    description = factory.Faker('sentence', nb_words=6)
    total = Decimal('100.00')
    tax = Decimal('10.00')
    currency = 'USD'
    delivery = Decimal('5.00')

    billing_first_name = factory.Faker('first_name')
    billing_last_name = factory.Faker('last_name')
    billing_address_1 = factory.Faker('street_address')
    billing_address_2 = ''
    billing_city = factory.Faker('city')
    billing_postcode = factory.Faker('postcode')
    billing_country_code = factory.LazyAttribute(lambda _: 'US')
    billing_country_area = factory.LazyAttribute(lambda _: 'NY')
    customer_ip_address = factory.LazyAttribute(lambda _: '127.0.0.1')

    # If BasePayment has any additional non-nullable fields (e.g. `status`, etc.),
    # you can override them here. By default, BasePayment auto-assigns status='waiting'
    # and sets created/modified timestamps automatically.
