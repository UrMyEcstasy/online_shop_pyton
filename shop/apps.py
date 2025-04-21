from django.apps import AppConfig


class ShopConfig(AppConfig):
    """
    Configuration class for the 'shop' application.

    Sets the default auto field type and application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
