#!/bin/bash
set -e

# Çevre değişkenlerinden kullanıcı, şifre ve veritabanı bilgilerini alın
POSTGRES_USER="${POSTGRES_USER}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"
POSTGRES_DB="${POSTGRES_DB}"

# Yeni bir veritabanı ve kullanıcı oluşturun
# Bu örnekte, mevcut POSTGRES_USER ve POSTGRES_DB kullanılıyor
# Yeni bir kullanıcı ve veritabanı oluşturmak yerine, bu örnek mevcutları kullanır

# (Opsiyonel) İlk veri yükleme veya schema oluşturma komutlarınızı buraya ekleyin
# Örneğin, bir tablo oluşturmak için:
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE IF NOT EXISTS my_table (
        id SERIAL PRIMARY KEY,
        column_name TYPE
    );
EOSQL