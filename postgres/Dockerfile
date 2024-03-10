# Resmi PostgreSQL imajını temel al
FROM postgres:latest

# COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY postgresql.conf /var/lib/postgresql/data/postgresql.conf

# COPY init-db.sh /docker-entrypoint-initdb.d/
COPY init-db.sh /docker-entrypoint-initdb.d/init-db.sh

# CMD ["postgres", "-c", "shared_buffers=256MB", "-c", "max_connections=200", "-g", "daemon off;"]

