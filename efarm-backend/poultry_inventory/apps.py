from django.apps import AppConfig


class PoultryInventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'poultry_inventory'

    def ready(self):
        import poultry_inventory.signals
