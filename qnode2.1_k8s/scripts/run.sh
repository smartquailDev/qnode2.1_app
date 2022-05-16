#!/bin/sh

set -e
APP_PORT=${PORT:-8000}
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"smartquail.info@gmail.com"}

python manage.py migrate --noinput
python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true

gunicorn --worker-tmp-dir /dev/shm qnode0_app.wsgi:application --bind "0.0.0.0:${APP_PORT}"

#uwsgi --socket :9000 --workers 4 --master --enable-threads --module qnode0_app.wsgi