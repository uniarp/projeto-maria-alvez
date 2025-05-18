FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]