from decouple import config

environment = config('DJANGO_ENVIRONMENT', default='development')
print(f"Current environment: {environment}")  # Add this line for debugging


if environment == 'production':
    from .prod import *
else:
    from .dev import *


