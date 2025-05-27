from django.apps import AppConfig


class ZoneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "zone"

    def ready(self):
        try: __import__(self.name, fromlist=['signals'])
        except ImportError: pass
