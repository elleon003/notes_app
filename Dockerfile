# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=app.settings.prod

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt --verbose

# Copy project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a startup script
RUN echo '#!/bin/sh' > /code/start.sh && \
    echo 'set -e' >> /code/start.sh && \
    echo 'until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do echo waiting for database; sleep 2; done;' >> /code/start.sh && \
    echo 'python manage.py migrate' >> /code/start.sh && \
    echo 'gunicorn app.wsgi:application --bind 0.0.0.0:8000' >> /code/start.sh && \
    chmod +x /code/start.sh

# Run the startup script
CMD ["/code/start.sh"]
