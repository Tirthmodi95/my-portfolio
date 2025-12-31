#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate --noinput

echo "from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Bunny@@1295')
    print('Superuser \"admin\" created successfully')
else:
    print('Superuser \"admin\" already exists')" | python manage.py shell
