#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

# Explicitly create migrations for core with verbosity
echo "Creating migrations for core..."
python manage.py makemigrations core --verbosity 2

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --noinput --verbosity 2

# Create admin user
echo "from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Bunny@@1295')
    print('Admin user created')
else:
    print('Admin user already exists')" | python manage.py shell