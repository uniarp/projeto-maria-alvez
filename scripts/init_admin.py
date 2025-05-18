import os
import django
from django.contrib.auth.models import User

# Configurar explicitamente o DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinica.settings')
django.setup()

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@clinica.com',
            password='admin123'
        )
        print("Superusuário 'admin' criado com sucesso!")
    else:
        print("Superusuário 'admin' já existe.")

if __name__ == '__main__':
    create_superuser()