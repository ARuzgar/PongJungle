# Dockerfile for a Django backend project

FROM python:3.9-slim

# Ortam değişkenlerini ayarla
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Uygulama kodunu kopyala
COPY . /app
RUN apt-get update && apt-get install -y postgresql-client

RUN pip install --no-cache-dir -r requirements.txt \
    && chmod +x automation.sh \
    && bash automation.sh

# Entrypoint scripti kopyala ve çalıştırılabilir yap
#COPY entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh

EXPOSE 9191

#ENTRYPOINT ["/entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:9191"]
