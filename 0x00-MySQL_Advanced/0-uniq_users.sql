-- Creates a table with unique users
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);