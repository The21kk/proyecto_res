const express = require('express');
const cors = require('cors');
const path = require('path');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const PORT = 3000;

// Configuración de la conexión a PostgreSQL
const pool = new Pool({
    user: process.env.DB_USER_METADATOS,
    host: process.env.DB_HOST_METADATOS,
    database: process.env.DB_NAME_METADATOS,
    password: process.env.DB_PASSWORD_METADATOS,
    port: process.env.DB_PORT_METADATOS,
});

app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

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

app.get('/api/robos', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM robos');
        res.json(result.rows);
    } catch (error) {
        console.error('Error al obtener los robos:', error);
        res.status(500).send('Error al obtener los robos');
    }
});

app.get('/api/reportes_trafico', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM reportes_trafico');
        res.json(result.rows);
    } catch (error) {
        console.error('Error al obtener los reportes de tráfico:', error);
        res.status(500).send('Error al obtener los reportes de tráfico');
    }
});

app.get('/api/estado_metro', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM estado_metro');
        res.json(result.rows);
    } catch (error) {
        console.error('Error al obtener el estado del metro:', error);
        res.status(500).send('Error al obtener el estado del metro');
    }
});

app.get('/api/feriados', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM feriados');
        res.json(result.rows);
    } catch (error) {
        console.error('Error al obtener los feriados:', error);
        res.status(500).send('Error al obtener los feriados');
    }
});

app.get('/api/informacion_extraida', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM informacion_extraida');
        res.json(result.rows);
    } catch (error) {
        console.error('Error al obtener la información extraída:', error);
        res.status(500).send('Error al obtener la información extraída');
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

// Inicia el servidor
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});

