#!/bin/sh

# Veritabanının hazır olup olmadığını kontrol et
until pg_isready -h ${POSTGRES_HOST_API} -U ${POSTGRES_USER_API} -p ${POSTGRES_PORT_API}; do
  >&2 echo "Veritabanı Api42 hazır değil - bekleniyor..."
  sleep 2
done

>&2 echo "Veritabanı hazır."

# Django migrasyonlarını çalıştır
python manage.py makemigrations
python manage.py migrate

# Uygulamayı başlat
exec "$@"