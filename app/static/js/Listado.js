// El arreglo avisosAdopcion ya NO se define aquí.
// Los datos se obtienen dinámicamente de la base de datos a través de la API de Flask.

// Función auxiliar para obtener los detalles del aviso de la API
async function obtenerDetallesAviso(avisoId) {
    try {
        const response = await fetch(`/api/aviso/${avisoId}`);
        if (!response.ok) {
            throw new Error('Aviso no encontrado en la base de datos.');
        }
        return await response.json();
    } catch (error) {
        console.error("Error al cargar detalles del aviso:", error);
        alert("No se pudo cargar la información detallada del aviso.");
        return null;
    }
}

// Función principal de inicialización
document.addEventListener('DOMContentLoaded', () => {

    const listaAvisosDiv = document.getElementById('lista-avisos');
    const detalleAvisoDiv = document.getElementById('detalle-aviso');
    const listadoPrincipal = document.getElementById('listado-principal');

    // Agrega un 'event listener' al listado principal.
    listadoPrincipal.addEventListener('click', async (event) => {
        // Identifica la fila (tr) más cercana al elemento clickeado.
        let filaClickeada = event.target.closest('tr');
        if (!filaClickeada) return;

        // Obtiene el ID del aviso desde el atributo 'data-id'.
        const avisoId = parseInt(filaClickeada.getAttribute('data-id'));
        if (isNaN(avisoId)) return;

        // Mostrar un mensaje de carga
        detalleAvisoDiv.innerHTML = '<p>Cargando detalles del aviso...</p>';
        
        // 1. Obtener los datos del aviso desde la API
        const aviso = await obtenerDetallesAviso(avisoId);
        
        if (!aviso) {
            // Si falla, volvemos a mostrar el listado y limpiamos el mensaje de error
            detalleAvisoDiv.innerHTML = '';
            listaAvisosDiv.style.display = 'block';
            return;
        }

        // 2. Oculta el listado y muestra la sección de detalles.
        listaAvisosDiv.style.display = 'none';
        detalleAvisoDiv.style.display = 'block';
        
        // Determinar la ruta de la foto (asumimos que siempre hay al menos una, aunque la API lo maneja)
        const fotoPrincipal = aviso.fotos && aviso.fotos.length > 0 ? aviso.fotos[0] : { src: '/static/img/default.jpg', alt: 'Sin foto' };


        // 3. Rellenar el HTML de detalles con datos de la DB
        detalleAvisoDiv.innerHTML = `
            <h2>Detalles del Aviso</h2>
            <p><strong>Fecha de Publicación:</strong> ${aviso.fechaPublicacion}</p>
            <p><strong>Fecha de Entrega:</strong> ${aviso.fechaEntrega}</p>
            <p><strong>Región:</strong> ${aviso.region}</p>
            <p><strong>Comuna:</strong> ${aviso.comuna}</p>
            <p><strong>Sector:</strong> ${aviso.sector || 'N/A'}</p>
            <p><strong>Cantidad/Tipo/Edad:</strong> ${aviso.cantidad} ${aviso.tipo}/${aviso.edad}</p>
            <p><strong>Nombre Contacto:</strong> ${aviso.nombreContacto}</p>
            <p><strong>Email:</strong> ${aviso.email}</p>
            <p><strong>Celular:</strong> ${aviso.celular || 'N/A'}</p>
            <p><strong>Contactar por:</strong> ${aviso.contactoPor}</p>
            <p><strong>Descripción:</strong> ${aviso.descripcion}</p>
            <div>
                <img class="foto-small" src="${fotoPrincipal.src}" alt="${fotoPrincipal.alt}" style="width: 320px; height: 240px; cursor: pointer; object-fit: cover;">
            </div>
            <br>
            <button id="volver-listado">Volver al listado</button>
            <button id="volver-portada">Volver a la portada</button>
        `;

        // 4. Agrega 'event listeners' a los botones "Volver al listado" y "Volver a la portada".
        document.getElementById('volver-listado').addEventListener('click', () => {
            detalleAvisoDiv.style.display = 'none';
            listaAvisosDiv.style.display = 'block';
        });

        document.getElementById('volver-portada').addEventListener('click', () => {
            window.location.href = 'index.html';
        });

        // 5. Agrega un 'event listener' para el clic en la foto pequeña.
        const fotoSmall = document.querySelector('.foto-small');
        if (fotoSmall) {
            fotoSmall.addEventListener('click', () => {
                // Crea un 'overlay' (superposición) para mostrar la imagen en grande.
                const overlay = document.createElement('div');
                overlay.className = 'overlay';
                overlay.style.cssText = `
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background-color: rgba(0, 0, 0, 0.9); display: flex; 
                    flex-direction: column; justify-content: center; align-items: center; 
                    z-index: 1000;
                `;
                overlay.innerHTML = `
                    <img src="${fotoPrincipal.src}" alt="${fotoPrincipal.alt}" style="max-width: 90%; max-height: 80%; object-fit: contain; margin-bottom: 20px;">
                    <button id="cerrar-foto" style="padding: 10px 20px; background-color: #f44336; color: white; border: none; cursor: pointer; border-radius: 5px;">Cerrar</button>
                `;
                document.body.appendChild(overlay);

                // Agrega un 'event listener' al botón para cerrar la superposición.
                document.getElementById('cerrar-foto').addEventListener('click', () => {
                    document.body.removeChild(overlay);
                });
            });
        }
    });
});