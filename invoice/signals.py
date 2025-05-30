# # booking/signals.py
# from django.dispatch import receiver
# from payments.signals import status_changed
# from payments import PaymentStatus
#
# from booking.choices import BookingStatusChoices
#
# @receiver(status_changed)
# def on_payment_status_changed(sender, instance, **kwargs):
#     if instance.status == PaymentStatus.CONFIRMED:
#         # mark booking confirmed
#         booking = instance.booking
#         booking.status = BookingStatusChoices.CONFIRMED.value
#         booking.save()
#
#         # # create invoice if not existing
#         # if not hasattr(booking, 'invoice'):
#         #     generate_invoice(booking)
