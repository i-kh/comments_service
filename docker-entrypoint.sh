#!/bin/sh

if [ "$1" = 'start' ]; then
  python manage.py migrate --noinput
  /usr/bin/supervisord -n

else
  exec "$@"
fi
