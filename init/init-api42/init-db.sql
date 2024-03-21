DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'apiusers') THEN
        CREATE DATABASE apiusers;
    END IF;
END
$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'api') THEN
        CREATE USER api WITH PASSWORD '123';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE backend TO user1;

ALTER ROLE user1 WITH SUPERUSER;
ALTER ROLE user1 WITH CREATEROLE;