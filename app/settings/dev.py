from .base import *
import logging


DEBUG = True

ALLOWED_HOSTS = [host.strip() for host in config('DJANGO_ALLOWED_HOSTS', default='').split(',') if host.strip()]


INSTALLED_APPS += ['django_browser_reload']
MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']

INTERNAL_IPS = [
    "127.0.0.1",
]
SECRET_KEY = 'django-insecure-(ct1m*p^^0)890$i)xy!q2k!w-zv=i!oi1_jdc$onps9b(ng4='

# Use console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'