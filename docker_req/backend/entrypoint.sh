#!/bin/sh

set -e

# Veritabanı bağlantı parametreleri
host="db"
port="5432"
user="${POSTGRES_USER}"
db="${POSTGRES_DB}"

# Veritabanının hazır olup olmadığını kontrol et
until PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$host" -U "$user" -d "$db" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# Migrasyonları çalıştır
python manage.py migrate

# Uygulamayı başlat
exec "$@"
