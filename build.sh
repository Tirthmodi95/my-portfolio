#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

# Run fresh migrations and create admin
python manage.py setupdb

# Optional: makemigrations in case of model changes
python manage.py makemigrations --noinput