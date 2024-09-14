# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Enforce correct settings
ENV DJANGO_SETTINGS_MODULE=app.settings.prod

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install psycopg2-binary==2.9.9 --no-cache-dir
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Creates a non-root user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Run entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]
