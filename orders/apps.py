from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Configuration class for the 'orders' application.

    Sets the default auto field type and application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'