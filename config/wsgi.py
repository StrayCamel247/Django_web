"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import sys
import os
from django.core.wsgi import get_wsgi_application


def setdefault_django_settings_module():
    from .constants import env
    # 设置django默认环境变量 DJANGO_SETTINGS_MODULE
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          'config.{}_settings'.format(env))


setdefault_django_settings_module()

application = get_wsgi_application()
