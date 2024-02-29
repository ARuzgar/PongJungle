# Dockerfile for a Django backend project

# Base image olarak Python 3.9 slim sürümünü kullan. Slim sürüm, boyutu azaltılmış ve gereksiz paketler çıkarılmıştır.
FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Çalışma dizinini oluştur ve ayarla
WORKDIR /app

# Uygulamanın bağımlılıklarını yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# (Django için genelde 8000 kullanılır ama bizim yaml dosyasında 8080)
EXPOSE 8080

# Uygulamayı çalıştırma komutu
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]

