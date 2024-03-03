# Base image olarak Python 3.9 slim sürümünü kullan
FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Çalışma dizinini oluştur ve ayarla
WORKDIR /app

# Önce requirements.txt dosyasını kopyala ve bağımlılıkları kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# automation.sh dosyasını kopyala ve çalıştırılabilir yap
COPY automation.sh .
RUN chmod +x automation.sh

# Uygulama kodunu kopyala
COPY . .

# automation.sh betiğini çalıştır
RUN bash automation.sh

# Uygulama için gerekli portu aç
EXPOSE 8080

# Django uygulamasını başlatma komutu
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
