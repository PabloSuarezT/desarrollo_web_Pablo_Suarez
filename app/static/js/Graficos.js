const API_URL_AVISOS_DIA = 'api/stats/avisos_por_dia';
const API_URL_TOTAL_TIPO = 'api/stats/total_por_tipo';
const API_URL_MENSUAL_TIPO = 'api/stats/mensual_por_tipo';

/**
 * Función genérica para obtener datos de cualquier endpoint.
 * @param {string} url - El endpoint de la API de Flask.
 * @param {string} containerId - El ID del div para mostrar el error.
 * @returns {Promise<any>} Promesa que resuelve con los datos JSON.
 */
async function obtenerDatos(url, containerId) {
    try {
        // La URL debe ser relativa al Blueprint 'main' o absoluta si no es parte del BP
        const fullUrl = url.startsWith('/') ? url : '/' + url; 
        const respuesta = await fetch(fullUrl);

        if (!respuesta.ok) {
            // Si el servidor retorna un error 500 o similar, mostramos el mensaje.
            throw new Error(`Error HTTP ${respuesta.status}: No se pudo obtener la data.`);
        }

        const datos = await respuesta.json();
        return datos;

    } catch (error) {
        console.error(`Error al cargar los datos de ${url}:`, error);
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = '<p style="color: red; text-align: center; font-family: sans-serif;">Error al cargar las estadísticas.</p>';
        }
        // Lanzamos el error para que la función de dibujo lo capture y detenga el proceso
        throw error;
    }
}


// ==============================================================================
// GRÁFICO 1: LÍNEAS (Avisos por Día)
// ==============================================================================

async function dibujarGraficoAvisosPorDia() {
    const containerId = 'chart-avisos-por-dia'; // ID del DIV en Estadistica.html
    try {
        const datos = await obtenerDatos(API_URL_AVISOS_DIA, containerId);

        // MODIFICACIÓN CRÍTICA: Asegurar que la fecha (primer elemento) sea un entero.
        // Esto previene errores si el JSON devuelve el timestamp como float o string.
        const datosHighcharts = datos.map(item => {
            // item[0] es el timestamp (fecha), item[1] es la cantidad
            return [parseInt(item[0], 10), item[1]]; 
        });

        Highcharts.chart(containerId, {
            chart: {
                type: 'line',
                zoomType: 'x', 
                style: { fontFamily: 'sans-serif' }
            },
            title: {
                text: '1. Cantidad de Avisos de Adopción por Día'
            },
            subtitle: {
                text: 'Gráfico de Líneas'
            },
            xAxis: {
                type: 'datetime', // CRÍTICO: Indica que el eje X son fechas (timestamps)
                title: {
                    text: 'Fecha de Ingreso'
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Cantidad de Avisos'
                },
                allowDecimals: false
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                // Formato que muestra la fecha con día, mes y año.
                pointFormat: '{point.y} avisos el {point.x:%e %b, %Y}' 
            },
            series: [{
                name: 'Avisos por Día',
                data: datosHighcharts, // Usamos los datos formateados
                color: '#5cb85c', // Verde
                lineWidth: 3,
                marker: {
                    symbol: 'circle'
                }
            }]
        });

    } catch (e) {
        // Error ya manejado y mostrado en obtenerDatos
        console.log('Fallo al dibujar el gráfico de Avisos por Día.');
    }
}


// ==============================================================================
// GRÁFICO 2: TORTA (Total por Tipo)
// ==============================================================================

async function dibujarGraficoTotalPorTipo() {
    const containerId = 'chart-total-por-tipo'; // ID del DIV en Estadistica.html
    try {
        // Los datos deben venir en formato: [{"name": "Gato", "y": 10}, {"name": "Perro", "y": 15}]
        const datos = await obtenerDatos(API_URL_TOTAL_TIPO, containerId);
        
        // Se asume que los datos están en español (Gato/Perro) desde el servidor.

        Highcharts.chart(containerId, {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie',
                style: { fontFamily: 'sans-serif' }
            },
            title: {
                text: '2. Total de Avisos por Tipo de Mascota'
            },
            subtitle: {
                text: 'Gráfico de Torta'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b> ({point.y} avisos)'
            },
            accessibility: {
                point: {
                    valueSuffix: '%'
                }
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                    },
                    showInLegend: true
                }
            },
            series: [{
                name: 'Porcentaje',
                colorByPoint: true,
                data: datos,
                // Asumiendo que el orden de datos es Gato, Perro o similar, asignamos colores fijos:
                colors: ['#00BFFF', '#FF4500'] // Azul para Gatos, Naranja/Rojo para Perros
            }]
        });

    } catch (e) {
        // Error ya manejado y mostrado en obtenerDatos
        console.log('Fallo al dibujar el gráfico de Torta.');
    }
}


// ==============================================================================
// GRÁFICO 3: BARRAS (Mensual por Tipo)
// ==============================================================================

async function dibujarGraficoMensualPorTipo() {
    const containerId = 'chart-mensual-por-tipo'; // ID del DIV en Estadistica.html
    try {
        // El API /api/stats/mensual_por_tipo devuelve un objeto con categorías y dos arrays de datos
        const data = await obtenerDatos(API_URL_MENSUAL_TIPO, containerId);

        Highcharts.chart(containerId, {
            chart: {
                type: 'column', // Gráfico de barras agrupadas
                style: { fontFamily: 'sans-serif' }
            },
            title: {
                text: '3. Avisos Mensuales por Tipo de Mascota'
            },
            subtitle: {
                text: 'Gráfico de Barras Agrupadas'
            },
            xAxis: {
                categories: data.categorias_x,
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Cantidad de Avisos'
                },
                allowDecimals: false
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [{
                name: 'Gatos',
                data: data.gatos,
                color: '#00BFFF'
            }, {
                name: 'Perros',
                data: data.perros,
                color: '#FF4500'
            }]
        });

    } catch (e) {
        // Error ya manejado y mostrado en obtenerDatos
        console.log('Fallo al dibujar el gráfico de Barras.');
    }
}


// Función principal que inicia la carga de todos los gráficos
document.addEventListener('DOMContentLoaded', () => {
    console.log("Cargando los 3 gráficos Highcharts...");
    // Estas tres funciones se ejecutan en paralelo
    dibujarGraficoAvisosPorDia();
    dibujarGraficoTotalPorTipo();
    dibujarGraficoMensualPorTipo();
});
