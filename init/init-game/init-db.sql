DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'game') THEN
        CREATE DATABASE game;
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'gameuser') THEN
        CREATE USER gameuser WITH PASSWORD '123';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE game TO gameuser;

ALTER ROLE gameuser WITH SUPERUSER;
ALTER ROLE gameuser WITH CREATEROLE;