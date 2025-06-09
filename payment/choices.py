from django.db import models


class PaymentMethodChoices(models.TextChoices):
    STRIPE = ('stripe', 'Stripe')
    CASH = ('cash', 'Cash')


class PaymentStatusChoices(models.TextChoices):
    CHARGE_SUCCEEDED = ('charge_succeeded', 'Charge Succeeded')
    CHARGE_CAPTURED = ('charge_captured', 'Charge Captured')
    ACTION_REQUIRED = ('action_required', 'Action Required')
    CHARGE_EXPIRED = ('charge_expired', 'Charge Expired')
    CHARGE_PENDING = ('charge_pending', 'Charge Pending')
    CHARGE_FAILED = ('charge_failed', 'Charge Failed')
    CAPTURABLE = ('capturable', 'Capturable')
    PROCESSING = ('processing', 'Processing')
    INITIATED = ('initiated', 'Initiated')
    CANCELLED = ('cancelled', 'Cancelled')
    SUCCEEDED = ('succeeded', 'Succeeded')
    REFUNDED = ('refunded', 'Refunded')
    DISPUTED = ('disputed', 'Disputed')
    FAILED = ('failed', 'Failed')
