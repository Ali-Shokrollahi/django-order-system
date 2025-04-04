#!/bin/bash
set -e  # Exit immediately on any error

echo "Applying database migrations..."
python manage.py migrate --noinput

# echo "Collecting static files..."
# python manage.py collectstatic --noinput

exec "$@"
