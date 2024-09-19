-- Проверка и создание базы данных
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'bot_database') THEN
        PERFORM pg_create_database('bot_database');
    END IF;
END
$$;

-- Проверка и создание пользователя
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'bot_user') THEN
        CREATE USER bot_user WITH PASSWORD 'password';
    END IF;
END
$$;

-- Назначение привилегий
GRANT ALL PRIVILEGES ON DATABASE bot_database TO bot_user;

-- Подключение к базе данных
\c bot_database

-- Создание таблиц
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    losers INT DEFAULT 0,
    nices INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS logs (
    date DATE PRIMARY KEY,
    loser VARCHAR(30) REFERENCES users(id),
    nice VARCHAR(30) REFERENCES users(id)
);
