# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy entrypoint script
COPY entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh

# Copy project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Debugging: List contents of /code
RUN ls -la /code
RUN cat /code/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/code/entrypoint.sh"]

# Set the default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
