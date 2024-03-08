# Base image olarak Python 3.9 slim sürümünü kullan
FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Çalışma dizinini oluştur
WORKDIR /app

# PostgreSQL client'ı kur
RUN apt-get update && apt-get install -y postgresql-client

# Bağımlılıkları kur
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Veritabanı migrasyonlarını yap
RUN python3 manage.py makemigrations

# Uygulama için gerekli portu aç
EXPOSE 9191
