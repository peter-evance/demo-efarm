from django.apps import AppConfig


class DairyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dairy'
    verbose_name_plural = 'Dairy Administration'

    def ready(self):
        import dairy.signals

