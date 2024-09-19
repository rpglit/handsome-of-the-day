-- create-db.sql

-- Создание базы данных
CREATE DATABASE bot_database;

-- Создание пользователя
CREATE USER bot_user WITH PASSWORD 'password';

-- Назначение привилегий
GRANT ALL PRIVILEGES ON DATABASE bot_database TO bot_user;


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
