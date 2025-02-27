# Use a imagem oficial do Python como base
FROM python:3.10

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o requirements.txt e instale as dependências
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Verificar se o Django foi instalado corretamente
RUN pip list

# Instalar psycopg2-binary para PostgreSQL
RUN pip install psycopg2-binary

# Copie o restante do código da aplicação
COPY . /app/

# Copie o entrypoint.sh para o diretório correto dentro do container
COPY entrypoint.sh /app/entrypoint.sh

# Tornar o entrypoint.sh executável
RUN chmod +x /app/entrypoint.sh

# Exponha a porta do servidor Django (8000)
EXPOSE 8000

# Defina variáveis de ambiente para o superusuário
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=projetoMariaAlvez.settings
ENV DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_EMAIL=admin@admin.com \
    DJANGO_SUPERUSER_PASSWORD=admin \
    DB_NAME=centro_de_bem_estar_maria_alvez \
    DB_USER=admin \
    DB_PASSWORD=adminadmin \
    DB_HOST=postgres_db \
    DB_PORT=5432

# Comando para rodar a aplicação Django
CMD ["sh", "-c", " \
    while ! pg_isready -h postgres_db -p 5432; do sleep 1; done && \
    python manage.py migrate && \
    python manage.py shell -c \"from django.contrib.auth.models import User; \
    User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() or \
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')\" && \
    python manage.py runserver 0.0.0.0:8000 \
"]