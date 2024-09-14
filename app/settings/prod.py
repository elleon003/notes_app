from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ALLOWED_HOSTS = ['notes-app-notes-app.xbekux.easypanel.host', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://notes-app-notes-app.xbekux.easypanel.host']


SECRET_KEY = config('SECRET_KEY')

# Use a more secure session cookie
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Email configuration (replace with your actual email settings)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

DATABASE_URL = config('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
}

STATIC_ROOT = '/app/staticfiles'
MEDIA_ROOT = '/app/media'


# Whitenoise for static file serving
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

