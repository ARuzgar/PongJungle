# Dockerfile for a Django backend project

FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Bağımlılıkları yükle
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY ./backend /app

EXPOSE 9191

# Entrypoint scripti kopyala ve çalıştırılabilir yap
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:9191"]
