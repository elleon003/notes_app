#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
gunicorn app.wsgi:application --bind 0.0.0.0:$PORT
