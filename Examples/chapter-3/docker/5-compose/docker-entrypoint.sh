#!/bin/sh

set -e

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

/var/venv/bin/python test-db-connection.py

# Apply database migrations
echo "Apply database migrations"
/var/venv/bin/python manage.py migrate

# Start server
echo "Starting server"
/var/venv/bin/python manage.py runserver 0.0.0.0:80
