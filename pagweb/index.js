const express = require('express');
const cors = require('cors');
const path = require('path');
const { Pool } = require('pg');
const fs = require('fs');
const csv = require('csv-parser');
require('dotenv').config({ path: './credentials.env' });

const app = express();
const PORT = 3000;

// Configuración de la conexión a PostgreSQL
const pool = new Pool({
    user: process.env.DB_USER_METADATOS,
    host: process.env.DB_HOST_METADATOS,
    database: process.env.DB_NAME_METADATOS,
    password: String(process.env.DB_PASSWORD_METADATOS),
    port: process.env.DB_PORT_METADATOS,
});

app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

// Función para normalizar los nombres (elimina tildes, convierte a minúsculas y recorta espacios)
const normalizeName = (name) => {
    return name
        .normalize("NFD") // Descompone caracteres con tilde
        .replace(/[\u0300-\u036f]/g, "") // Elimina marcas de tilde
        .toLowerCase()
        .trim(); // Convierte a minúsculas y elimina espacios extra
};

// Rutas para cargar datos específicos desde la base de datos
app.get('/api/museos', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM museos_scraping');
        res.json(result.rows);
    } catch (error) {
        console.error('Error al obtener los museos:', error);
        res.status(500).send('Error al obtener los museos');
    }
});

// Rutas para los archivos GeoJSON
app.get('/capa1', (req, res) => {
    res.sendFile(path.join(__dirname, 'data', 'capa1.geojson'));
});

app.get('/capa2', (req, res) => {
    res.sendFile(path.join(__dirname, 'data', 'capa2.geojson'));
});

app.get('/comunas', (req, res) => {
    res.sendFile(path.join(__dirname, 'data', '13.geojson'));
});

// Ruta para simular fallas a partir del CSV de probabilidades
app.get('/simular-fallas', (req, res) => {
    const filePath = path.join(__dirname, 'data', 'nodos_museos_probabilidades.csv');
    const { inicio, fin } = req.query; // Nodos de inicio y fin desde la solicitud
    const nodos = [];

    if (!inicio || !fin) {
        return res.status(400).send('Se requieren parámetros de inicio y fin');
    }

    fs.createReadStream(filePath)
        .pipe(csv())
        .on('data', (row) => {
            if (row.nodo_id === inicio || row.nodo_id === fin) { // Filtrar por nodos de inicio y fin
                const probabilidadFallo = parseFloat(row.probabilidad_fallo);
                const randomValue = Math.random() * 100; // Generar un número aleatorio entre 0 y 100
                const falla = randomValue < (probabilidadFallo * 100); // Comparar con el umbral

                nodos.push({
                    nodo_id: row.nodo_id,
                    lat: parseFloat(row.lat),
                    lon: parseFloat(row.lon),
                    probabilidad_fallo: probabilidadFallo,
                    falla: falla, // true si ocurre la falla, false en caso contrario
                });
            }
        })
        .on('end', () => {
            res.json(nodos); // Solo devolver los nodos filtrados
        })
        .on('error', (err) => {
            console.error('Error al leer el archivo CSV:', err);
            res.status(500).send('Error al procesar el archivo CSV');
        });
});

// Ruta para mostrar probabilidades de amenazas desde el CSV generado
app.get('/api/probabilidades-amenazas', (req, res) => {
    const filePath = path.join(__dirname, 'data', 'amenazas_probabilidades.csv');
    const geoJsonPath = path.join(__dirname, 'data', 'capa1.geojson');
    const { inicio, fin } = req.query;

    if (!inicio || !fin) {
        return res.status(400).send('Se requieren parámetros de inicio y fin');
    }

    // Leer el archivo GeoJSON y construir el diccionario de museos
    const geojsonData = JSON.parse(fs.readFileSync(geoJsonPath, 'utf8'));
    const museoCoords = {};

    geojsonData.features.forEach((feature) => {
        const nombre = normalizeName(feature.properties.nombre);
        const [lon, lat] = feature.geometry.coordinates;
        museoCoords[nombre] = { lat, lon };
    });

    // Normalizar los nombres proporcionados en la solicitud
    const inicioNormalized = normalizeName(inicio);
    const finNormalized = normalizeName(fin);

    const inicioCoords = museoCoords[inicioNormalized];
    const finCoords = museoCoords[finNormalized];

    // Logs para depuración
    console.log('Inicio:', inicio, 'Normalizado:', inicioNormalized, 'Coordenadas:', inicioCoords);
    console.log('Fin:', fin, 'Normalizado:', finNormalized, 'Coordenadas:', finCoords);

    if (!inicioCoords || !finCoords) {
        return res.status(404).send('Nombres de museos no encontrados en el GeoJSON');
    }

    // Leer el CSV y filtrar por coordenadas
    const resultados = [];
    fs.createReadStream(filePath)
        .pipe(csv())
        .on('data', (row) => {
            const rowLat = parseFloat(row.lat);
            const rowLon = parseFloat(row.lon);

            // Comparar coordenadas con tolerancia
            if (
                (Math.abs(rowLat - inicioCoords.lat) < 0.0001 && Math.abs(rowLon - inicioCoords.lon) < 0.0001) ||
                (Math.abs(rowLat - finCoords.lat) < 0.0001 && Math.abs(rowLon - finCoords.lon) < 0.0001)
            ) {
                resultados.push(row);
            }
        })
        .on('end', () => {
            res.json(resultados);
        })
        .on('error', (err) => {
            console.error('Error al leer el archivo CSV:', err);
            res.status(500).send('Error al procesar el archivo CSV');
        });
});


console.log('Variables cargadas desde .env:', {
    user: process.env.DB_USER_METADATOS,
    host: process.env.DB_HOST_METADATOS,
    database: process.env.DB_NAME_METADATOS,
    password: process.env.DB_PASSWORD_METADATOS,
    port: process.env.DB_PORT_METADATOS,
});

// Inicia el servidor
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});

