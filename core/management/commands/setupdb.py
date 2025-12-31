from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Run migrations and create admin user'

    def handle(self, *args, **options):
        self.stdout.write("Running migrations...")
        call_command('migrate', verbosity=0)

        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'Bunny@@1295')
            self.stdout.write(self.style.SUCCESS('Admin user created: admin / Bunny@@1295'))
        else:
            self.stdout.write('Admin user already exists')

        self.stdout.write(self.style.SUCCESS('Setup complete!'))