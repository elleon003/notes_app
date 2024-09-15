#!/bin/sh

set -e

cd /app

# Ensure proper permissions
chmod -R 755 /app/staticfiles

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py create_default_superuser

exec gunicorn --bind :8000 --workers 3 app.wsgi:application
