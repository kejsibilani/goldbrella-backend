from django.apps import AppConfig


class ShiftConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shift"

    def ready(self):
        try: __import__(self.name, fromlist=['signals'])
        except ImportError: pass
