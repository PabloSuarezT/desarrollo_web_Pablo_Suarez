document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('adoption-form');
    const message = document.getElementById('message');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Evita el envío tradicional del formulario

        // Simulación de validación y envío de datos
        if (form.checkValidity()) {
            // Muestra mensaje de éxito
            message.textContent = "¡Gracias por tu solicitud! La revisaremos pronto.";
            message.className = 'success';
            message.classList.remove('hidden');

            // Opcional: Deshabilitar el formulario y limpiarlo
            form.reset();
            form.querySelector('button[type="submit"]').disabled = true;
        } else {
            // Este caso es poco probable si se usan atributos 'required', 
            // pero es un buen fallback.
            message.textContent = "Por favor, completa todos los campos requeridos.";
            message.className = 'error';
            message.classList.remove('hidden');
        }
    });
});