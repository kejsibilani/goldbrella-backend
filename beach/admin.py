from django.contrib import admin
from beach.models import Beach, BeachImage, Menu, MenuImage

@admin.register(Beach)
class BeachAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "code", "location")
    search_fields = ('title', 'location__city')
    list_filter = ('location',)

@admin.register(BeachImage)
class BeachImageAdmin(admin.ModelAdmin):
    list_display = ('beach', 'image', 'created')
    search_fields = ('beach__title',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "beach", "title")
    search_fields = ('title', 'beach__title')
    list_filter = ('beach',)

@admin.register(MenuImage)
class MenuImageAdmin(admin.ModelAdmin):
    list_display = ('menu', 'image', 'created')
    search_fields = ('menu__title',)
