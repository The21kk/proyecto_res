-- Conectarse al servidor PostgreSQL y crear las bases de datos

-- Crear la base de datos museos_db
CREATE DATABASE museos_db OWNER postgres;

-- Crear la base de datos monumentos_db
CREATE DATABASE monumentos_db OWNER postgres;

-- Crear la base de datos edges_SQL
CREATE DATABASE edges_SQL OWNER postgres;

-- Conceder privilegios al usuario postgres
GRANT ALL PRIVILEGES ON DATABASE museos_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE monumentos_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE edges_SQL TO postgres;

-- Crear la tabla Edges_SQL en edges_SQL
\c edges_SQL;  -- Cambiar a la base de datos edges_SQL

CREATE TABLE Edges_SQL (
    id SERIAL PRIMARY KEY,
    source_id INT NOT NULL,
    target_id INT NOT NULL,
    weight FLOAT,
    description TEXT
);

-- Mensaje de éxito
RAISE NOTICE 'Las bases de datos museos_db, monumentos_db y edges_SQL han sido creadas exitosamente, junto con la tabla Edges_SQL.';
