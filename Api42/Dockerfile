# Base image olarak Python 3.9 slim sürümünü kullan
FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

# PostgreSQL client'ı (pg_isready için) ve diğer bağımlılıkları yükle
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl


COPY . .

EXPOSE 8080

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY cloudflare_cache_clear.sh /cloudflare_cache_clear.sh

RUN chmod +x /cloudflare_cache_clear.sh

ENTRYPOINT ["/entrypoint.sh"]
