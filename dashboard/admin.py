from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models import User
# from beach.models import Beach  # Already registered in beach/admin.py
# from beach.models import BeachImage  # Already registered in beach/admin.py
from beach.models import BeachOpeningHour
from beach.models import BeachOpeningSeason
from booking.models import BookedInventory
# from booking.models import Booking  # Already registered in booking/admin.py
# from booking.models import SunbedBooking  # Already registered in booking/admin.py
# from inventory.models import InventoryItem  # Already registered in inventory/admin.py
from location.models import Location
from mailer.models import ScheduledEmail
from services.models import Facility
from services.models import Rule
from shift.models import Shift
# from sunbed.models import Sunbed  # Already registered in sunbed/admin.py
from zone.models import Zone


# Register your models here.
class UserAdmin(BaseUserAdmin):
    pass


# class SunbedAdmin(admin.ModelAdmin):  # Already defined in sunbed/admin.py
#     list_display = ("id", "zone", "price")
#     # search_fields = ("beach__title", "status")
#     # list_filter = ("beach__title")
#     # readonly_fields = ("status",)


# class SunbedBookingAdmin(admin.ModelAdmin):  # Already defined in booking/admin.py
#     list_display = ("id", "booking", "sunbed")
#     # search_fields = ("booking__user__username", "sunbed__id")
#     # list_filter = ("booking__booking_date", "sunbed__status")


# Registering all models
admin.site.register(User, UserAdmin)
# admin.site.register(SunbedBooking, SunbedBookingAdmin)  # Already registered in booking/admin.py
# admin.site.register(Sunbed, SunbedAdmin)  # Already registered in sunbed/admin.py

admin.site.register(Shift)
admin.site.register(Location)
admin.site.register(BeachOpeningHour)
admin.site.register(BeachOpeningSeason)
# admin.site.register(BeachImage)  # Already registered in beach/admin.py
# admin.site.register(Beach)  # Already registered in beach/admin.py
admin.site.register(Zone)
# admin.site.register(InventoryItem)  # Already registered in inventory/admin.py
# admin.site.register(Booking)  # Already registered in booking/admin.py
admin.site.register(BookedInventory)
admin.site.register(Facility)
admin.site.register(Rule)

admin.site.register(ScheduledEmail)
