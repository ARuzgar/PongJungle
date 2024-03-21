#!/bin/sh

# Veritabanının hazır olup olmadığını kontrol et
until pg_isready -h ${POSTGRES_HOST_BACKEND} -p ${POSTGRES_PORT_BACKEND} -U ${POSTGRES_USER_BACKEND}; do
  >&2 echo "Veritabanı hazır değil - bekleniyor..."
  sleep 2
done

>&2 echo "Veritabanı hazır."

# Django migrasyonlarını çalıştır
python manage.py migrate

# Uygulamayı başlat
exec "$@"