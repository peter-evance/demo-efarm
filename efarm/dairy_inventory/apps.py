from django.apps import AppConfig


class DairyInventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dairy_inventory'

    def ready(self):
        import dairy_inventory.signals
