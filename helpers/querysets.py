from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from account.models import User
from beach.models import Beach, BeachOpeningSeason
from booking.models import Booking
from inventory.models import InventoryItem
from invoice.models import BookingInvoice
from location.models import Location
from services.models import Facility, Rule
from sunbed.models import Sunbed
from zone.models import Zone


def zone_queryset(request):
    return Zone.objects.all()


def beach_location_queryset(request):
    return Location.objects.all()


def beach_season_queryset(request):
    return BeachOpeningSeason.objects.all()


def beach_queryset(request):
    return Beach.objects.all()


def facilities_queryset(request):
    return Facility.objects.all()


def rules_queryset(request):
    return Rule.objects.all()


def sunbed_queryset(request):
    return Sunbed.objects.all()


def inventory_queryset(request):
    return InventoryItem.objects.all()


def user_queryset(request):
    if request.user.is_superuser:
        return User.objects.all()
    elif request.user.is_staff:
        return User.objects.filter(
            Q(
                role='guest',
                pk=request.user.pk,
                _connector=Q.OR
            )
        )
    return User.objects.filter(pk=request.user.pk)


def supervisor_queryset(request):
    return User.objects.filter(role='supervisor')


def staff_queryset(request):
    return User.objects.filter(role='staff')


def management_queryset(request):
    return User.objects.filter(Q(Q(role='staff'), Q(role='supervisor'), _connector=Q.OR))


def self_user_queryset(request):
    return User.objects.filter(pk=request.user.pk)


def booking_queryset(request):
    if request.user.is_superuser:
        return Booking.objects.all()
    elif request.user.is_staff:
        return Booking.objects.filter(
            Q(booked_by=request.user.pk, user=request.user.pk, _connector=Q.OR)
        )
    return Booking.objects.filter(user=request.user.pk)


def invoice_queryset(request):
    if request.user.is_superuser:
        return BookingInvoice.objects.all()
    elif request.user.is_staff:
        return BookingInvoice.objects.filter(
            Q(booking__booked_by=request.user.pk, booking__user=request.user.pk, _connector=Q.OR)
        )
    return BookingInvoice.objects.filter(booking__user=request.user.pk)


def complaint_related_queryset(request):
    return ContentType.objects.filter(
        model__in=[
            'inventoryitem', 'sunbed'
        ]
    )
