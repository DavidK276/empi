#!/bin/bash

# Wait for database to be up
while :
do
    (echo -n > /dev/tcp/db/5432) >/dev/null 2>&1
    if [[ $? -eq 0 ]]; then
        break
    fi
    sleep 1
done

set -euo pipefail

cd /app/empi-server
chown appuser:appuser .django_secret
chmod 600 .django_secret

poetry run ./manage.py migrate
poetry run ./manage.py createinitialuser --noinput

if [ ${DEBUG:+1} ]; then
  exec poetry run ./manage.py runserver 0.0.0.0:8000
else
  exec poetry run gunicorn empi_server.wsgi --bind 127.0.0.1:8001 --workers 4 --max-requests 1000
fi