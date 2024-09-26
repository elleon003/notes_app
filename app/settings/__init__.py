from decouple import config
from django.conf import settings

environment = config('DJANGO_ENVIRONMENT', default='development')
print(f"Current environment: {environment}")  # Add this line for debugging


if environment == 'production':
    from .prod import *
else:
    from .dev import *


