CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    pidrs INT DEFAULT 0,
    nices INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS logs (
    date DATE PRIMARY KEY,
    pidr INT REFERENCES users(id),
    nice INT REFERENCES users(id)
);
