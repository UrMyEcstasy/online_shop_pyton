import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_online_shop.settings')

#: ASGI application callable for Django project.
application = get_asgi_application()

