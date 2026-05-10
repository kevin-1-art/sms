FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install \
    gunicorn==21.2.0 \
    django-redis==5.4.0 \
    psycopg2-binary==2.9.9 \
    whitenoise==6.6.0 \
    python-decouple==3.8 \
    boto3==1.34.0 \
    django-storages==1.14.2 \
    sentry-sdk==1.38.0

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/logs

# Collect static files
RUN python manage.py collectstatic --noinput --settings=config.settings_production 2>/dev/null || true

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/', timeout=2)" || exit 1

# Run gunicorn
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "config.wsgi:application"]
