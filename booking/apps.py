from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "booking"

    def ready(self):
        try: __import__(self.name, fromlist=['signals'])
        except ImportError: pass
