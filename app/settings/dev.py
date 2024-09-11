from .base import *
import logging

logging.basicConfig(level=logging.DEBUG)

DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INTERNAL_IPS = [
    "127.0.0.1",
]
SECRET_KEY = 'django-insecure-(ct1m*p^^0)890$i)xy!q2k!w-zv=i!oi1_jdc$onps9b(ng4='

# Use console email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'