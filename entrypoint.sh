#!/bin/sh

set -e

cd /app

python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
python manage.py create_default_superuser

exec gunicorn --bind :8000 --workers 3 app.wsgi:application
