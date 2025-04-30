from django.apps import AppConfig


class BeachConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beach'

    def ready(self):
        try: __import__(self.name, fromlist=['signals'])
        except ImportError: pass
