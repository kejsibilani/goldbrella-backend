from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from account.models import User
from beach.models import Beach, BeachLocation, BeachOpeningHour, BeachImage, BeachOpeningSeason
from booking.models import SunbedBooking, Booking
from inventory.models import InventoryItem
from payment.models import BookingPayment
from services.models import Facility, Rule
from sunbed.models import Sunbed


# Register your models here.
class UserAdmin(BaseUserAdmin):
    pass


class SunbedAdmin(admin.ModelAdmin):
    list_display = ("id", "beach", "price")
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

admin.site.register(Beach)
admin.site.register(BeachImage)
admin.site.register(BeachLocation)
admin.site.register(BeachOpeningHour)
admin.site.register(BeachOpeningSeason)
admin.site.register(InventoryItem)
admin.site.register(Booking)
admin.site.register(BookingPayment)
admin.site.register(Facility)
admin.site.register(Rule)
