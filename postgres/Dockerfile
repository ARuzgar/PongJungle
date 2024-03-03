# Resmi PostgreSQL imajını temel al
FROM postgres:latest

COPY postgresql.conf /var/lib/tmp

CMD ["postgres", "-c", "shared_buffers=256MB", "-c", "max_connections=200"]
