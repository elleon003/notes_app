echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
gunicorn app.wsgi:application --bind 0.0.0.0:8000