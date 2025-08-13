from django.contrib import admin
from sunbed.models import Sunbed

@admin.register(Sunbed)
class SunbedAdmin(admin.ModelAdmin):
    list_display = ("id", "zone", "area", "identity", "row", "column", "price", "status", "created")
    search_fields = ("identity", "area", "zone__beach__title")
    list_filter = ("zone", "status")
