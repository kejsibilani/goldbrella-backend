from django.contrib import admin
from notification.models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created')
    search_fields = ('user__email', 'message')
    list_filter = ('is_read', 'created')
