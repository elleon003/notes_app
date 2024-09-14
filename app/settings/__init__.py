from decouple import config

# Default to using the development settings
environment = config('DJANGO_ENVIRONMENT', default='development')

if environment == 'production':
    from .prod import *
elif environment == 'development':
    from .dev import *
else:
    raise ValueError(f"Unknown environment: {environment}")
