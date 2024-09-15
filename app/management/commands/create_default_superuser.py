from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config


class Command(BaseCommand):
    help = 'Creates a superuser if none exist'

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).count() == 0:
            email = config('DJANGO_SUPERUSER_EMAIL')
            password = config('DJANGO_SUPERUSER_PASSWORD')
            
            User.objects.create_superuser(email=email, password=password)
            
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" was created'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
