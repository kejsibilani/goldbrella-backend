import factory
from payments import PaymentStatus

from payment.factories.payment import BookingPaymentFactory


class StripePaymentFactory(BookingPaymentFactory):
    variant = "stripe"
    status = PaymentStatus.WAITING

    @factory.post_generation
    def skip_stripe_api(self, create, extracted, **kwargs):
        if not create:
            return
        # Do nothing. Don’t call get_form_data().
