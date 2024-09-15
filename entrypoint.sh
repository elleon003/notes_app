#!/bin/sh

set -e

cd /app

# Collect static files directly to STATIC_ROOT, ignoring errors
python manage.py collectstatic --noinput --no-post-process -i *.gz -i *.br || true

# Run migrations
python manage.py migrate --noinput

# Create superuser
python manage.py create_default_superuser

# Start Gunicorn
exec gunicorn --bind :8000 --workers 3 app.wsgi:application
