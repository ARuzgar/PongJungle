#!/bin/sh

# Veritabanının hazır olup olmadığını kontrol et
until pg_isready -h ${POSTGRES_HOST_GAME} -p ${POSTGRES_PORT_GAME} -U ${POSTGRES_USER_GAME}; do
  >&2 echo "Veritabanı Game hazır değil - bekleniyor..."
  sleep 2
done

>&2 echo "Veritabanı hazır."

# Django migrasyonlarını çalıştır
python manage.py makemigrations
python manage.py migrate

# Uygulamayı başlat
exec "$@"