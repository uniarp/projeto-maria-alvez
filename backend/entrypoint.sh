#!/bin/bash

# Verifica se as variáveis de ambiente essenciais estão definidas
if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ]; then
    echo "Erro: Variáveis de ambiente DB_HOST ou DB_PORT não definidas"
    exit 1
fi

# O healthcheck no docker-compose.yml já garante que o PostgreSQL está pronto
echo "PostgreSQL está pronto (verificado pelo healthcheck do Docker)!"

# Rodar as migrações do Django
echo "Executando migrações do Django..."
python manage.py migrate --noinput

# Verificar e criar superusuário se necessário
echo "Verificando/criando superusuário Django..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
username = "$DJANGO_SUPERUSER_USERNAME"
email = "$DJANGO_SUPERUSER_EMAIL"
password = "$DJANGO_SUPERUSER_PASSWORD"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superusuário criado com sucesso!")
else:
    print("Superusuário já existe.")
EOF

# Executar o comando passado como argumento, se houver, ou iniciar o servidor por padrão
if [ $# -gt 0 ]; then
    echo "Executando comando: $@"
    exec "$@"
else
    echo "Iniciando o servidor Django em 0.0.0.0:8000..."
    exec python manage.py runserver 0.0.0.0:8000
fi