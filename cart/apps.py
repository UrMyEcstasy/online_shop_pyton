from django.apps import AppConfig


class CartConfig(AppConfig):
    """
    Configuration class for the 'cart' application.

    Specifies the default auto field type and application name.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
