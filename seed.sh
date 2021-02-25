#!/bin/bash
rm -rf todoapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations todoapi
python manage.py migrate todoapi
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata my_user
python manage.py loaddata task