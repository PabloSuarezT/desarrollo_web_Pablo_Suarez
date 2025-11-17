document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('adoption-form');
    const message = document.getElementById('message');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); 


        if (form.checkValidity()) {

            message.textContent = "¡Gracias por tu solicitud! La revisaremos pronto.";
            message.className = 'success';
            message.classList.remove('hidden');

            form.reset();
            form.querySelector('button[type="submit"]').disabled = true;
        } else {
            message.textContent = "Por favor, completa todos los campos requeridos.";
            message.className = 'error';
            message.classList.remove('hidden');
        }
    });
});