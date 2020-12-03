"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

from django.core.asgi import get_asgi_application

from .handler import setdefault_django_settings_module

setdefault_django_settings_module()

application = get_asgi_application()
