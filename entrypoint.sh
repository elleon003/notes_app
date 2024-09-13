#!/usr/bin/env bash

# Ensure we're in the correct directory
cd /app

# # Activate the PDM environment
# source .venv/bin/activate

# Run the commands
python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn -b :8000 app.wsgi
