from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models import User
from beach.models import Beach
from beach.models import BeachImage
from beach.models import BeachOpeningHour
from beach.models import BeachOpeningSeason
from booking.models import BookedInventory
from booking.models import Booking
from booking.models import SunbedBooking
from inventory.models import InventoryItem
from location.models import Location
from mailer.models import ScheduledEmail
from services.models import Facility
from services.models import Rule
from shift.models import Shift
from sunbed.models import Sunbed
from zone.models import Zone


# Register your models here.
class UserAdmin(BaseUserAdmin):
    pass


class SunbedAdmin(admin.ModelAdmin):
    list_display = ("id", "zone", "price")
    # search_fields = ("beach__title", "status")
    # list_filter = ("beach__title")
    # readonly_fields = ("status",)


class SunbedBookingAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "sunbed")
    # search_fields = ("booking__user__username", "sunbed__id")
    # list_filter = ("booking__booking_date", "sunbed__status")


# Registering all models
admin.site.register(User, UserAdmin)
admin.site.register(SunbedBooking, SunbedBookingAdmin)
admin.site.register(Sunbed, SunbedAdmin)

admin.site.register(Shift)
admin.site.register(Location)
admin.site.register(BeachOpeningHour)
admin.site.register(BeachOpeningSeason)
admin.site.register(BeachImage)
admin.site.register(Beach)
admin.site.register(Zone)
admin.site.register(InventoryItem)
admin.site.register(Booking)
admin.site.register(BookedInventory)
admin.site.register(Facility)
admin.site.register(Rule)

admin.site.register(ScheduledEmail)
