from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Cria um superusuário admin se ele não existir'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@clinica.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS("Superusuário 'admin' criado com sucesso!"))
        else:
            self.stdout.write(self.style.WARNING("Superusuário 'admin' já existe."))