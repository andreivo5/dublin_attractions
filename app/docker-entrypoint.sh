#!/bin/bash
 
# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate
 
# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input
 
# Start uWSGI
echo "Starting uWSGI..."
uwsgi --ini /app/uwsgi.ini