#!/bin/bash

python wait_for_pg.py
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"