#!/bin/bash
APP_PORT=${PORT:-8000}
gunicorn --worker-tmp-dir /dev/shm qnode0_app.wsgi:application --bind "0.0.0.0:${APP_PORT}"