#!/bin/bash
# Production startup script for Citizen Hub Kenya Backend

echo "Starting Citizen Hub Kenya Backend in production mode..."

# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn -c gunicorn_config.py citizenhub.wsgi:application
