FROM python:3-slim

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser

# Create directories with correct permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

# Copy project files and set permissions
COPY --chown=appuser:appuser . .

# Set environment variable for static files
ENV STATIC_ROOT /app/staticfiles
ENV STATIC_TEMP /app/static_temp
ENV DJANGO_ENVIRONMENT production


# Switch to non-root user
USER appuser

# Make sure the entrypoint is executable
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
