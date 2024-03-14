#!/bin/sh

set -e

# Veritabanı bağlantı parametreleri
port="5432"
user="${POSTGRES_USER}"
db="${POSTGRES_DB}"

# Veritabanının hazır olup olmadığını kontrol et
until PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "127.0.0.1" -U "$user" -d "$db" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

if [ $? -ne 0 ]; then
  echo "Database veya tablo bulunamadı. Skript sonlandırılıyor."
  exit 1
else
  echo "Postgres bağlantısı başarılı."
fi

>&2 echo "Postgres is up - executing command"

# Migrasyonları çalıştır
python manage.py migrate

# Uygulamayı başlat
exec "$@"
