from django.apps import AppConfig


class SunbedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sunbed'

    def ready(self):
        try: __import__(self.name, fromlist=['signals'])
        except ImportError: pass
