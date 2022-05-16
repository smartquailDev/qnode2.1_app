#!/bin/sh
set -e

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"smartquail.info@gmail.com"}

python manage.py migrate --noinput
python manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true