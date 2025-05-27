from django.apps import AppConfig


class LocationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "location"

    def ready(self):
        try: __import__(self.name, fromlist=['signals'])
        except: pass
