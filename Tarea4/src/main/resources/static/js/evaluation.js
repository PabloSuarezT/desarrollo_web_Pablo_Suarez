document.addEventListener('DOMContentLoaded', () => {
    
    const modal = document.getElementById('evaluation-modal');
    const form = document.getElementById('evaluation-form');
    const notaInput = document.getElementById('nota-input');
    const modalAvisoId = document.getElementById('modal-aviso-id');
    const modalErrorMessage = document.getElementById('modal-error-message');
    const messageContainer = document.getElementById('message-container');
    const cancelButton = document.getElementById('cancel-evaluation-btn');
    
    let currentAvisoId = null;

    // --- Funciones de Utilidad ---

    function displayMessage(type, content) {
        messageContainer.innerHTML = ''; // Limpiar mensajes anteriores
        const msgDiv = document.createElement('div');
        
        msgDiv.style.padding = '10px';
        msgDiv.style.borderRadius = '5px';
        msgDiv.style.fontWeight = 'bold';

        if (type === 'success') {
            msgDiv.style.backgroundColor = '#d4edda';
            msgDiv.style.color = '#155724';
            msgDiv.textContent = ' Éxito: ' + content;
        } else if (type === 'error') {
            msgDiv.style.backgroundColor = '#f8d7da';
            msgDiv.style.color = '#721c24';
            msgDiv.textContent = ' Error: ' + content;
        } else if (type === 'validation') {
            modalErrorMessage.style.display = 'block';
            modalErrorMessage.textContent = content;
            return;
        }
        messageContainer.appendChild(msgDiv);
        
        // Limpiar el mensaje después de 5 segundos
        setTimeout(() => {
            messageContainer.innerHTML = '';
        }, 5000);
    }
    
    // Función para cerrar el modal
    function closeModal() {
        modal.style.display = 'none';
        notaInput.value = ''; 
        modalErrorMessage.style.display = 'none'; // Ocultar errores del modal
    }

    // --- Event Handlers ---

    // 1. Mostrar Modal al hacer clic en 'evaluar'
    document.querySelectorAll('.btn-evaluar').forEach(button => {
        button.addEventListener('click', (event) => {
            currentAvisoId = event.target.dataset.avisoId;
            modalAvisoId.textContent = `(ID: ${currentAvisoId})`;
            modal.style.display = 'flex'; // Mostrar el modal
            notaInput.focus();
        });
    });

    // 2. Cancelar la evaluación
    cancelButton.addEventListener('click', closeModal);

    // 3. Manejar el envío del formulario (Reemplaza la lógica del prompt)
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        modalErrorMessage.style.display = 'none';
        
        const notaValor = parseInt(notaInput.value);

        // Validación de la nota (sin prompt/alert)
        if (isNaN(notaValor) || notaValor < 1 || notaValor > 7) {
            displayMessage('validation', 'Debe ingresar un número entero entre 1 y 7.');
            return;
        }

        // Construir la URL del endpoint API con los parámetros de consulta
        const apiUrl = `/api/evaluar?avisoId=${currentAvisoId}&valorNota=${notaValor}`;

        try {
            // Realizar la llamada asíncrona (POST, sin cuerpo, ya que los datos van en la URL)
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                // Se envía un cuerpo vacío si no se usa @RequestBody
                body: JSON.stringify({}) 
            });

            if (response.ok) {
                const nuevoPromedio = await response.json(); 
                
                // Actualizar la celda de la tabla
                const promedioCell = document.getElementById(`promedio-${currentAvisoId}`);
                const promedioTexto = nuevoPromedio !== null ? nuevoPromedio.toFixed(2) : '-';
                
                if (promedioCell) {
                    promedioCell.textContent = promedioTexto;
                }
                
                closeModal();
                displayMessage('success', `Nota ${notaValor} guardada con éxito. Nuevo promedio: ${promedioTexto}`);

            } else if (response.status === 400) {
                // Error de validación del servidor (nota fuera de rango, etc.)
                displayMessage('error', 'Error de validación. La nota debe ser un número entre 1 y 7.');
                
            } else {
                // Otros errores del servidor (500)
                const errorBody = await response.text(); 
                displayMessage('error', `Error del servidor: [${response.status}] No se pudo guardar la nota.`);
            }

        } catch (error) {
            console.error("Error en la evaluación:", error);
            displayMessage('error', 'Ocurrió un error de conexión al intentar guardar la nota.');
        }
    });
});