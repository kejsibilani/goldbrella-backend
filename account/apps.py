from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        try: __import__(self.name, fromlist=['signals'])
        except ImportError: pass
