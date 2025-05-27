CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth1234';

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

CREATE DATABASE auth;

USE auth;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

INSERT INTO user (email, password) VALUES ('admin@gmail.com', 'Admin1234')
