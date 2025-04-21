from django.apps import AppConfig

"""
 Configuration class for the 'accounts' application.

 Sets the default auto field and identifies the application by name.
 """

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
