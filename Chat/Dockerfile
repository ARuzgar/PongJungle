# Base image olarak Python 3.9 slim sürümünü kullan
FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Çalışma dizinini oluştur ve ayarla
WORKDIR /app

# PostgreSQL client'ı kur
RUN apt-get update && apt-get install -y postgresql-client

# Önce requirements.txt ve automation.sh dosyasını kopyala
COPY requirements.txt ./

# Bağımlılıkları kur ve automation.sh betiğini çalıştır
RUN pip install --no-cache-dir -r requirements.txt 

# Uygulama kodunu kopyala
COPY . .

# Uygulama için gerekli portu aç
EXPOSE 9090
