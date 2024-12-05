# Use a imagem oficial do Python como base
FROM python:3.10-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Instalar dependências de sistema necessárias para psycopg2 (conector do PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie o requirements.txt e instale as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Verificar se o Django foi instalado corretamente
RUN pip list

# Instalar psycopg2-binary para PostgreSQL
RUN pip install psycopg2-binary

# instalando o netcat 
RUN apt-get update && apt-get install -y netcat-openbsd

# Copie o restante do código da aplicação
COPY . /app/

# Exponha a porta do servidor Django (8000)
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

# Defina variáveis de ambiente para o superusuário (recomendação: não deixar no Dockerfile para produção)
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
CMD ["sh", "-c", "python manage.py migrate && \
    python manage.py shell -c \"from django.contrib.auth.models import User; \
    User.objects.filter(username='admin').exists() or \
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')\" && \
    python manage.py runserver 0.0.0.0:8000"]

    