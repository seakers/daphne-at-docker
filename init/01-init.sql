CREATE DATABASE daphne;
\c daphne;
CREATE USER daphne WITH PASSWORD 'daphnetest';
GRANT ALL PRIVILEGES ON DATABASE daphne TO daphne;