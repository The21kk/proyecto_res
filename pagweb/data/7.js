function verificarFallo(probabilidadFallo) {
    const randomValue = Math.random() * 100;
    
    // Verificar si la conexión falla o no
    if (randomValue <= probabilidadFallo * 100) {
        return true;
    } else {
        return false;
    }
}

// Ejemplo de uso
/*const conexiones = [

];*/
module.exports = function verificarFallo(conexiones) {
    // Contenido de la función
};


conexiones.forEach(conexion => {
    const falla = verificarFallo(conexion.failureProbability);
    console.log(`Conexión de ${conexion.from} a ${conexion.to}: ${falla ? "Falla" : "Disponible"}`);
});
