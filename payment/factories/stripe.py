import factory

from payment.choices import PaymentMethodChoices
from payment.choices import PaymentStatusChoices
from payment.factories.payment import BookingPaymentFactory


class StripePaymentFactory(BookingPaymentFactory):
    """
    Factory for BookingPayment with payment_method='STRIPE'.
    Inherits all fields (including amount == invoice.total_amount)
    but overrides payment_method.
    """
    payment_method = PaymentMethodChoices.STRIPE.value
    status = PaymentStatusChoices.INITIATED.value

    # Generate a realistic Stripe PaymentIntent ID and matching client_secret
    external_intent = factory.Sequence(lambda n: f"pi_{n:08d}")
    client_secret   = factory.LazyAttribute(lambda o: f"{o.external_intent}_secret")
