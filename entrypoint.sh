#!/bin/bash

# Espera até o banco de dados PostgreSQL estar disponível
echo "Aguardando o banco de dados iniciar..."
until nc -z -v -w30 $DB_HOST $DB_PORT; do
  echo "Aguardando o PostgreSQL iniciar..."
  sleep 1
done

# Rodar as migrações do Django
echo "Rodando migrações..."
python manage.py migrate

# Verificar e criar superusuário se necessário
echo "Verificando superusuário..."
python manage.py shell -c "from django.contrib.auth.models import User; \
    User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or \
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"

# Rodar o servidor Django
echo "Iniciando o servidor Django..."
python manage.py runserver 0.0.0.0:8000
