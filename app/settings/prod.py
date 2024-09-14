from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'notes.s9apps.com']
CSRF_TRUSTED_ORIGINS = ['localhost', '127.0.0.1', 'notes.s9apps.com']

SECRET_KEY = config('SECRET_KEY')

# Use a more secure session cookie
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTPS settings
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

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

# Whitenoise for static file serving
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'