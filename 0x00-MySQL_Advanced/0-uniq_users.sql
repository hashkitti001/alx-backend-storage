-- Creates a table with unique users

DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);