"""
WSGI config for one_click_convert project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

DJANGO_ENV = os.getenv("DJANGO_ENV", "production")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"one_click_convert.settings.{DJANGO_ENV}")

application = get_wsgi_application()
