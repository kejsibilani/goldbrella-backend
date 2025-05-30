# from decimal import Decimal
# from django.shortcuts import get_object_or_404, redirect
# from payments import get_payment_model
# from booking.models import Booking
#
# Payment = get_payment_model()
#
# def pay_for_booking(request, booking_pk):
#     booking = get_object_or_404(Booking, pk=booking_pk)
#
#     # calculate your total (e.g. per-sunbed price)
#     total = sum(sb.price for sb in booking.sunbeds.all())
#
#     payment = Payment.objects.create(
#         variant='default',
#         description=f'Booking #{booking.pk} at {booking.beach.title}',
#         total=Decimal(total),
#         currency='EUR',
#         billing_first_name=request.user.first_name,
#         billing_last_name=request.user.last_name,
#         customer_ip_address=request.META.get('REMOTE_ADDR'),
#         booking=booking
#     )
#     # hands off to the provider (Stripe checkout, PayPal, etc.)
#     return redirect(payment.get_process_url())
#
# # booking/views.py
# from django.http import FileResponse
# from .models import Invoice
#
# def download_invoice(request, booking_pk):
#     invoice = get_object_or_404(Invoice, booking__pk=booking_pk)
#     return FileResponse(invoice.pdf, as_attachment=True,
#                         filename=f'invoice_{booking_pk}.pdf')
