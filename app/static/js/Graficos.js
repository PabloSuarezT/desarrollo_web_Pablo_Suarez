// Espera a que el DOM esté completamente cargado para ejecutar el código.
document.addEventListener('DOMContentLoaded', () => {

    // --- Configuración del Gráfico de Línea ---
    const dataLinea = {
        // Etiquetas para el eje X (días de la semana).
        labels: ['Día 1', 'Día 2', 'Día 3', 'Día 4', 'Día 5', 'Día 6', 'Día 7'],
        datasets: [{
            label: 'Cantidad de Avisos de Adopción',
            // Datos del gráfico.
            data: [5, 8, 4, 10, 7, 9, 6],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
            fill: false
        }]
    };

    const configLinea = {
        type: 'line', // Tipo de gráfico: línea.
        data: dataLinea,
        options: {
            responsive: true, // El gráfico se ajusta al tamaño del contenedor.
            plugins: {
                title: {
                    display: true,
                    text: 'Avisos de Adopción por Día' // Título del gráfico.
                }
            }
        }
    };
    // Crea una nueva instancia del gráfico de línea en el elemento con el ID 'graficoLinea'.
    new Chart(document.getElementById('graficoLinea'), configLinea);

    // --- Configuración del Gráfico de Pastel (Torta) ---
    const dataTorta = {
        // Etiquetas para cada sector (Perros y Gatos).
        labels: ['Perros', 'Gatos'],
        datasets: [{
            label: 'Total de Avisos por Tipo',
            data: [20, 15],
            // Colores para cada sector.
            backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)'],
            hoverOffset: 4
        }]
    };

    const configTorta = {
        type: 'pie', // Tipo de gráfico: pastel.
        data: dataTorta,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Total de Avisos por Tipo de Mascota' // Título del gráfico.
                }
            }
        }
    };
    // Crea una nueva instancia del gráfico de pastel en el elemento con el ID 'graficoTorta'.
    new Chart(document.getElementById('graficoTorta'), configTorta);

    // --- Configuración del Gráfico de Barras ---
    const dataBarras = {
        // Etiquetas para el eje X (meses).
        labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
        datasets: [
            {
                label: 'Perros',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: 'rgb(255, 99, 132)'
            },
            {
                label: 'Gatos',
                data: [8, 15, 6, 10, 5, 8],
                backgroundColor: 'rgb(54, 162, 235)'
            }
        ]
    };

    const configBarras = {
        type: 'bar', // Tipo de gráfico: barras.
        data: dataBarras,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Avisos por Tipo y Mes' // Título del gráfico.
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Cantidad de Avisos' // Título del eje Y.
                    }
                }
            }
        }
    };
    // Crea una nueva instancia del gráfico de barras en el elemento con el ID 'graficoBarras'.
    new Chart(document.getElementById('graficoBarras'), configBarras);
});