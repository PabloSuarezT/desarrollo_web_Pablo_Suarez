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

        // 1. Obtener el ID del aviso (DEBE SER LO PRIMERO)
        const avisoId = parseInt(filaClickeada.getAttribute('data-id'));
        if (isNaN(avisoId)) return;

        // Mostrar un mensaje de carga antes de la llamada a la API
        detalleAvisoDiv.innerHTML = '<p>Cargando detalles del aviso...</p>';
        listaAvisosDiv.style.display = 'none'; // Ocultar listado inmediatamente
        detalleAvisoDiv.style.display = 'block'; // Mostrar contenedor de detalle
        
        // 2. Obtener los datos del aviso desde la API (AWAIT NECESARIO)
        const aviso = await obtenerDetallesAviso(avisoId);
        
        if (!aviso) {
            // Si falla, volvemos a mostrar el listado y limpiamos el mensaje de error
            detalleAvisoDiv.innerHTML = '<h2>Error al cargar el aviso</h2><button id="volver-listado-error">Volver al listado</button>';
             document.getElementById('volver-listado-error').addEventListener('click', () => {
                detalleAvisoDiv.style.display = 'none';
                listaAvisosDiv.style.display = 'block';
            });
            return;
        }

        // 3. GENERAR HTML (AHORA QUE TENEMOS LA VARIABLE 'aviso' con los datos)
        
        // Determinar la ruta de la foto principal y generar HTML para TODAS las fotos
        const fotoPrincipal = aviso.fotos && aviso.fotos.length > 0 ? aviso.fotos[0] : { src: '/static/img/default.jpg', alt: 'Sin foto' };

        const fotosHTML = aviso.fotos.map(foto => `
            <img class="clickable-image" 
                 src="${foto.src}" 
                 alt="${foto.alt}" 
                 data-full-src="${foto.src}"
                 style="width: 100px; height: 100px; cursor: pointer; object-fit: cover; margin: 5px;">
        `).join('');


        // 🟢 CÓDIGO AÑADIDO: Generar el HTML para la lista de contactos
        // NOTA: aviso.contactosDetalle viene de la API de Flask
        const contactosHTML = aviso.contactosDetalle.map(contacto => `
            <li><strong>${contacto.metodo}:</strong> ${contacto.identificador}</li>
        `).join('');
        // -------------------------------------------------------------


        // 4. Rellenar el HTML de detalles
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
            
            
            <p><strong>Todos los Contactos:</strong></p>
            <ul style="list-style: disc; margin-left: 20px;">
                ${contactosHTML}
            </ul>
            <p><strong>Descripción:</strong> ${aviso.descripcion}</p>
            
            <div id="fotos-galeria" style="display: flex; flex-wrap: wrap; margin-bottom: 15px;">
                ${fotosHTML}
            </div>

            <br>
            <button id="volver-listado">Volver al listado</button>
            <button id="volver-portada">Volver a la portada</button>
            
            <section class="comentarios-section">
                <h2>Comentarios</h2>
                
                <div id="comentario-messages" class="alert-message"></div>

                <div class="comentario-form-container">
                    <h3>Deja tu comentario</h3>
                    <form id="comentario-form">
                        <div>
                            <label for="comentario-nombre">Tu Nombre:</label>
                            <input type="text" id="comentario-nombre" required maxlength="80">
                        </div>
                        <div>
                            <label for="comentario-texto">Comentario:</label>
                            <textarea id="comentario-texto" rows="4" required maxlength="500"></textarea>
                        </div>
                        <button type="submit">Comentar</button>
                    </form>
                </div>

                <div id="comentarios-lista">
                    </div>
            </section>
        `;

        // 5. Agrega 'event listeners' a los botones de navegación
        document.getElementById('volver-listado').addEventListener('click', () => {
            detalleAvisoDiv.style.display = 'none';
            listaAvisosDiv.style.display = 'block';
        });

        document.getElementById('volver-portada').addEventListener('click', () => {
            window.location.href = 'index.html';
        });

        // =========================================================
        // 6. Lógica de Overlay/Zoom de Foto (Aplicar a la nueva galería)
        // =========================================================
        
        // Aplicamos el listener directamente al contenedor y delegamos
        const fotosGaleria = document.getElementById('fotos-galeria');
        if (fotosGaleria) {
            fotosGaleria.addEventListener('click', (event) => {
                const target = event.target;
                if (target.classList.contains('clickable-image')) {
                    const src = target.getAttribute('data-full-src');
        
                    const overlay = document.createElement('div');
                    overlay.className = 'overlay';
                    overlay.style.cssText = `
                        position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                        background-color: rgba(0, 0, 0, 0.9); display: flex; 
                        flex-direction: column; justify-content: center; align-items: center; 
                        z-index: 1000;
                    `;
                    overlay.innerHTML = `
                        <img src="${src}" alt="${target.alt}" style="max-width: 90%; max-height: 80%; object-fit: contain; margin-bottom: 20px;">
                        <button id="cerrar-foto" style="padding: 10px 20px; background-color: #f44336; color: white; border: none; cursor: pointer; border-radius: 5px;">Cerrar</button>
                    `;
                    document.body.appendChild(overlay);
        
                    document.getElementById('cerrar-foto').addEventListener('click', () => {
                        document.body.removeChild(overlay);
                    });
                }
            });
        }
        
        // =========================================================
        // 7. Lógica de Comentarios (Funcionalidad de API POST/GET)
        // =========================================================

        // Función para cargar los comentarios existentes
        const cargarComentarios = async (avisoId) => {
            const comentariosListaDiv = document.getElementById('comentarios-lista');
            comentariosListaDiv.innerHTML = '<p>Cargando comentarios...</p>';
            try {
                const response = await fetch(`/api/comentarios/${avisoId}`);
                if (!response.ok) throw new Error('Error al cargar comentarios.');

                const comentarios = await response.json();
                
                if (comentarios.length === 0) {
                    comentariosListaDiv.innerHTML = '<p>Sé el primero en comentar.</p>';
                } else {
                    comentariosListaDiv.innerHTML = comentarios.map(c => `
                        <div class="comentario-item">
                            <p><strong>${c.nombre}</strong> <span class="comentario-fecha">(${c.fecha})</span></p>
                            <p>${c.texto}</p>
                        </div>
                    `).join('');
                }
            } catch (error) {
                console.error("Error al cargar comentarios:", error);
                comentariosListaDiv.innerHTML = '<p style="color: red;">No se pudieron cargar los comentarios.</p>';
            }
        };

        // Llama a cargarComentarios inmediatamente después de mostrar el aviso
        cargarComentarios(avisoId);
        
        // 8. Configurar el envío del formulario de comentario
        const comentarioForm = document.getElementById('comentario-form');
        const comentarioMessages = document.getElementById('comentario-messages');
        
        comentarioForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Evita el envío tradicional del formulario

            const nombreInput = document.getElementById('comentario-nombre');
            const textoInput = document.getElementById('comentario-texto');
            
            const nombre = nombreInput.value.trim();
            const comentario = textoInput.value.trim();
            
            // Validaciones básicas (mantenidas del código anterior)
            if (nombre.length < 3 || nombre.length > 80) {
                comentarioMessages.style.display = "block";
                comentarioMessages.textContent = '❌ El nombre debe tener entre 3 y 80 caracteres.';
                comentarioMessages.className = 'alert-message error';
                return;
            }
            if (comentario.length < 5 || comentario.length > 500) {
                comentarioMessages.style.display = "block";
                comentarioMessages.textContent = '❌ El comentario debe tener entre 5 y 500 caracteres.';
                comentarioMessages.className = 'alert-message error';
                return;
            }

            try {
                const response = await fetch(`/api/comentarios/${avisoId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json' 
                    },
                    body: JSON.stringify({
                        nombre: nombre, 
                        comentario: comentario 
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Error desconocido al guardar el comentario.');
                }
                
                // Éxito: Limpia el formulario y recarga los comentarios
                nombreInput.value = '';
                textoInput.value = '';
                
                comentarioMessages.style.display = "block";
                comentarioMessages.textContent = '✅ Comentario agregado con éxito.';
                comentarioMessages.className = 'alert-message success';
                
                cargarComentarios(avisoId); // Recarga para ver el nuevo comentario

            } catch (error) {
                console.error("Error al enviar el comentario:", error);
                comentarioMessages.style.display = "block";
                comentarioMessages.textContent = `❌ Falló el envío: ${error.message}`;
                comentarioMessages.className = 'alert-message error';
            }
        });
    }); // Cierre del listadoPrincipal.addEventListener('click')
    
}); // Cierre de document.addEventListener('DOMContentLoaded')