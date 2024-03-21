# Base image olarak Python 3.9 slim sürümünü kullan
FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1

# Çalışma dizinini oluştur
WORKDIR /code

# PostgreSQL client'ı (pg_isready için) ve diğer bağımlılıkları yükle
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kur
COPY requirements.txt .

RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Uygulama için gerekli portu aç
EXPOSE 9191

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
