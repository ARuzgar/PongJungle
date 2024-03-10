# Dockerfile for a Django backend project

# Base image olarak Python 3.9 slim sürümünü kullan. Slim sürüm, boyutu azaltılmış ve gereksiz paketler çıkarılmıştır.
FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Çalışma dizinini oluştur ve ayarla
WORKDIR /app

COPY requirements.txt .
COPY automation.sh .

# Uygulama kodunu kopyala
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x automation.sh \
    && bash automation.sh



#(Django için genelde 8000 kullanılır ama bizim yaml dosyasında 9090)
EXPOSE 9090

# Uygulamayı çalıştırma komutu
CMD ["python3", "manage.py", "runserver", "0.0.0.0:9090"]