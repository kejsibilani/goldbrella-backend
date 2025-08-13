from django.contrib import admin
from inventory.models import InventoryItem

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'beach', 'price', 'quantity', 'reusable_item', 'created')
    search_fields = ('name', 'beach__title')
    list_filter = ('category', 'beach')
