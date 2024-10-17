const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.static(path.join(__dirname, 'public')));

// Rutas para los archivos GeoJSON
app.get('/capa1', (req, res) => {
    res.sendFile(path.join(__dirname, 'data', 'capa1.geojson'));
});

app.get('/capa2', (req, res) => {
    res.sendFile(path.join(__dirname, 'data', 'capa2.geojson'));
});

// Inicia el servidor
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
