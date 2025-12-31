#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

# Force fresh migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create admin user if not exists
echo "from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Bunny@@1295')
    print('Admin user created')
else:
    print('Admin user already exists')" | python manage.py shell