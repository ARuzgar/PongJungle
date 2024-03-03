# Base image olarak Python 3.9 slim sürümünü kullan
FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Çalışma dizinini oluştur ve ayarla
WORKDIR /app

# Önce requirements.txt ve automation.sh dosyasını kopyala
COPY requirements.txt automation.sh ./

# Bağımlılıkları kur ve automation.sh betiğini çalıştır
RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x automation.sh \
    && ./automation.sh

# Uygulama kodunu kopyala
COPY . .

# Uygulama için gerekli portu aç
EXPOSE 5050

# Uygulamayı çalıştırma komutu
CMD ["python3", "manage.py", "runserver", "0.0.0.0:5050"]
