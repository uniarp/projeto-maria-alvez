# Use a imagem oficial do Python como base
FROM python:3.10-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Copie o requirements.txt e instale as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . /app/

# Exponha a porta do servidor Django (8000)
EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=projetoclinica.settings

# Defina variáveis de ambiente para o superusuário
ENV DJANGO_SUPERUSER_USERNAME=arthur \
    DJANGO_SUPERUSER_EMAIL=arthur@arthur.com \
    DJANGO_SUPERUSER_PASSWORD=admin

# Executar migrações e criar superusuário
RUN python manage.py migrate && python start.py || true

# Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]