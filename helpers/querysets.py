from django.db.models import Q

from account.models import User
from beach.models import BeachLocation, Beach, BeachOpeningSeason
from services.models import Facility, Rule
from sunbed.models import Sunbed


def beach_location_queryset(request):
    return BeachLocation.objects.all()


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


def user_queryset(request):
    if request.user.is_superuser:
        return User.objects.all()
    elif request.user.is_staff:
        return User.objects.filter(
            Q(
                Q(is_staff=False, is_superuser=False, _connector=Q.AND),
                Q(pk=request.user.pk),
                _connector=Q.OR
            )
        )
    return User.objects.filter(pk=request.user.pk)
