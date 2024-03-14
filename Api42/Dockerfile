# Base image olarak Python 3.9 slim sürümünü kullan
FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080