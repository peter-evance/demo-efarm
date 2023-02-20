from django.apps import AppConfig


class DairyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dairy'

    def ready(self):
        import dairy.signals