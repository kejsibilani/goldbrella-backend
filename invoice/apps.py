from django.apps import AppConfig


class InvoiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "invoice"

    def ready(self):
        try: __import__(self.name, fromlist=['signals'])
        except ImportError: pass
