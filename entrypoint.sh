#!/bin/sh

set -e

cd /app

# Collect static files to a temporary directory
python manage.py collectstatic --noinput --clear --no-post-process -i *.gz -i *.br --settings=app.settings.temp_static

# Move collected files to the final static directory
rm -rf ${STATIC_ROOT}/*
cp -r ${STATIC_TEMP}/* ${STATIC_ROOT}/

python manage.py migrate --noinput
python manage.py create_default_superuser

exec gunicorn --bind :8000 --workers 3 app.wsgi:application
