// Definir la probabilidad de fallos para diferentes tipos de amenazas
const threatProbabilities = {
    "feriado": 0.05,       // Cierre completo en días feriados
    "robos": 0.3,          // Áreas con robos frecuentes
    "cierre_metro": 0.23,  // Cierre de estaciones de metro cercanas
    "cierre_calle": 0.7    // Cierre de calles cercanas
};

// Función para calcular la probabilidad de fallo dado un conjunto de amenazas
function calculateFailureProbability(threats) {
    let failureProbability = 1;

    for (let threat of threats) {
        let threatProb = threatProbabilities[threat] || 0;
        failureProbability *= (1 - threatProb);
    }

    return 1 - failureProbability;
}

// Datos de ejemplo de `ruta` y `museos`
// `ruta` representa las conexiones entre museos y sus pesos
// `museos` contiene los detalles de cada museo, incluyendo las amenazas asociadas

const ruta = [
    { from: 1, to: 2, weight: 10 },
    { from: 2, to: 3, weight: 15 },
    { from: 1, to: 3, weight: 20 },
    // Añade más conexiones según sea necesario
];

const museos = [
    { id: 1, nombre: 'Museo A', threats: ['feriado'] },
    { id: 2, nombre: 'Museo B', threats: ['robos', 'cierre_calle'] },
    { id: 3, nombre: 'Museo C', threats: [] },
    // Añade más museos según sea necesario
];

// Función para generar la probabilidad de fallo entre las rutas de museos
function generateFailureProbability(ruta, museos) {
    const failureData = [];

    for (let conexion of ruta) {
        let startNode = museos.find(m => m.id === conexion.from);
        let endNode = museos.find(m => m.id === conexion.to);

        let startFailure = calculateFailureProbability(startNode.threats);
        let endFailure = calculateFailureProbability(endNode.threats);
        
        let routeFailureProbability = 1 - ((1 - startFailure) * (1 - endFailure));

        failureData.push({
            from: startNode.nombre,
            to: endNode.nombre,
            weight: conexion.weight,
            failureProbability: routeFailureProbability.toFixed(2)
        });
    }

    return failureData;
}

// Generar las probabilidades de fallo para las rutas
const failureProbabilityData = generateFailureProbability(ruta, museos);
console.log("Probabilidades de fallo en rutas:", failureProbabilityData);

// Exportar los datos para que `index.js` los utilice en la API
module.exports = failureProbabilityData;

