import os
from decouple import config

# Default to using the base settings
settings_module = 'app.settings.base'

if config('DJANGO_ENVIRONMENT') == 'production':
    settings_module = 'app.settings.prod'
elif config('DJANGO_ENVIRONMENT') == 'development':
    settings_module = 'app.settings.dev'

# Use exec() to dynamically import the appropriate settings module
exec(f"from {settings_module} import *")