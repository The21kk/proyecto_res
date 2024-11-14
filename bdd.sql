-- Conectarse al servidor PostgreSQL y crear las bases de datos

-- Crear la base de datos museos_db
CREATE DATABASE museos_db OWNER boris;

-- Crear la base de datos monumentos_db
CREATE DATABASE monumentos_db OWNER boris;

-- Crear la base de datos edges_SQL
CREATE DATABASE edges_SQL OWNER boris;

-- Conceder privilegios al usuario boris en las bases de datos existentes
GRANT ALL PRIVILEGES ON DATABASE museos_db TO boris;
GRANT ALL PRIVILEGES ON DATABASE monumentos_db TO boris;
GRANT ALL PRIVILEGES ON DATABASE edges_sql TO boris;


-- Crear la base de datos 'metadatos'
CREATE DATABASE metadatos OWNER boris;
GRANT ALL PRIVILEGES ON DATABASE metadatos TO boris;

-- Conectarse a la base de datos 'metadatos' para crear las tablas
\c metadatos

CREATE TABLE IF NOT EXISTS edges_sql (
    id SERIAL PRIMARY KEY,
    source INT NOT NULL,           -- Nodo de inicio
    target INT NOT NULL,           -- Nodo de fin
    cost FLOAT,                    -- Peso (distancia) en la dirección source -> target
    reverse_cost FLOAT,            -- Peso en la dirección opuesta, o un valor alto si es unidireccional
    description TEXT               -- Descripción opcional
);

CREATE TABLE IF NOT EXISTS nodes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    lat FLOAT,
    lon FLOAT
);

-- Crear la tabla 'robos'
CREATE TABLE IF NOT EXISTS robos (
    id SERIAL PRIMARY KEY,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    robos INT
);

-- Crear la tabla 'reportes_trafico'
CREATE TABLE IF NOT EXISTS reportes_trafico (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME,
    descripcion TEXT,
    enlace TEXT
);

-- Crear la tabla 'estado_metro'
CREATE TABLE IF NOT EXISTS estado_metro (
    id SERIAL PRIMARY KEY,
    nombre_estacion VARCHAR(100) NOT NULL,
    estado VARCHAR(50)
);

-- Crear la tabla 'feriados'
CREATE TABLE IF NOT EXISTS feriados (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    nombre VARCHAR(100),
    irrenunciable BOOLEAN,
    tipo VARCHAR(50),
    leyes TEXT
);

-- Crear la tabla 'informacion_extraida'
CREATE TABLE IF NOT EXISTS informacion_extraida (
    id SERIAL PRIMARY KEY,
    url TEXT,
    ficha_informacion TEXT,
    article_titulo TEXT
);

-- Crear la tabla 'museos_scraping'
CREATE TABLE IF NOT EXISTS museos_scraping (
    id SERIAL PRIMARY KEY,
    museum_names VARCHAR(255),
    museum_ratings NUMERIC,
    museum_reviews FLOAT
);

-- Instrucciones COPY para cargar los datos desde CSV, omitiendo la columna id

COPY robos(lat, lon, robos) FROM '/home/nicolas/Desktop/U/proyecto_res/Amenazas/robos.csv' DELIMITER ',' CSV HEADER;
COPY reportes_trafico(fecha, hora, descripcion, enlace) FROM '/home/nicolas/Desktop/U/proyecto_res/Amenazas/reportes_trafico.csv' DELIMITER ',' CSV HEADER;
COPY estado_metro(nombre_estacion, estado) FROM '/home/nicolas/Desktop/U/proyecto_res/Amenazas/estado_metro.csv' DELIMITER ',' CSV HEADER;
COPY feriados(nombre, fecha, irrenunciable, tipo, leyes) FROM '/home/nicolas/Desktop/U/proyecto_res/Amenazas/feriados_chile2024.csv' DELIMITER ',' CSV HEADER;
COPY informacion_extraida(url, ficha_informacion, article_titulo) FROM '/home/nicolas/Desktop/U/proyecto_res/Metadata/informacion_extraida.csv' DELIMITER ',' CSV HEADER;
COPY museos_scraping(museum_names, museum_ratings, museum_reviews) FROM '/home/nicolas/Desktop/U/proyecto_res/Metadata/museos_Scraping.csv' DELIMITER ',' CSV HEADER;
