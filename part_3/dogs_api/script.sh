#!/bin/bash

pylint app --disable=E1101 --recursive y -E
if [ $? -gt 0 ]
then
  exit 1
fi

python manage.py migrate
export DJANGO_SUPERUSER_EMAIL=admin@admin.com
export DJANGO_SUPERUSER_PASSWORD=admin
export DJANGO_SUPERUSER_USERNAME=admin
python manage.py createsuperuser --no-input

gunicorn --bind 0.0.0.0:8008 config.wsgi