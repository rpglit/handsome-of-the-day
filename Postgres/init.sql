CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    losers INT DEFAULT 0,
    nices INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS logs (
    date DATE PRIMARY KEY,
    loser INT REFERENCES users(id),
    nice INT REFERENCES users(id)
);
