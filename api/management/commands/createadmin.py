from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
  help = "Create a superuser account with username=admin and password=admin."

  def handle(self, *args, **options):
    username = "admin"
    password = "admin"
    User.objects.create_superuser(username=username, password=password)
    self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))