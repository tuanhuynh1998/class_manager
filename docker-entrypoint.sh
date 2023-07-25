#!/bin/sh
set -e

if [ "$RUN_MIGRATIONS" = '1' ] 
then
  echo "Migrating..."
  python manage.py migrate
  echo "Collecting static..."
  python manage.py collectstatic --no-input
fi


exec "$@"
