document.addEventListener('DOMContentLoaded', () => {

    const regionSelect = document.getElementById('region');
    const comunaSelect = document.getElementById('comuna');
    const contactSelect = document.getElementById('contacto-por-select');
    // Este contenedor será el padre de los inputs dinámicos
    const contactContainer = document.getElementById('otro-contacto-contenedor');
    
    const formulario = document.querySelector('form');
    const cantidadInput = document.getElementById('cantidad');
    const edadInput = document.getElementById('edad');
    const tipoSelect = document.getElementById('tipo');
    const unidadEdadSelect = document.getElementById('unidad-edad');
    const fechaEntregaInput = document.getElementById('fecha-entrega');
    const agregarFotoBtn = document.getElementById('agregar-foto');
    const fotosContainer = document.getElementById('fotos-container');
    const nombreInput = document.getElementById('nombre');
    const emailInput = document.getElementById('email');
    const celularInput = document.getElementById('celular');
    const sectorInput = document.getElementById('sector');
    
    const validations = document.createElement("div");
    validations.style.display = "none",
    formulario.prepend(validations);

    // --- LÓGICA DINÁMICA DE REGIONES Y COMUNAS (USANDO FLASK API) ---
    
    // NOTA: Asumimos que las regiones ya están cargadas estáticamente en el HTML
    // (Renderizadas por Flask al cargar Adopcion.html con Jinja2).
    
    // Función para cargar comunas vía AJAX
    const cargarComunas = async (regionId) => {
        comunaSelect.innerHTML = '<option value="" disabled selected>Cargando comunas...</option>';
        comunaSelect.disabled = true;

        if (!regionId) {
            comunaSelect.innerHTML = '<option value="" disabled selected>Seleccione una región</option>';
            comunaSelect.disabled = false;
            return;
        }

        try {
            // Llama al endpoint de Flask que creaste
            const response = await fetch(`/comunas/${regionId}`);
            
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            
            const comunas = await response.json();

            // Limpiar y rellenar el select de comunas
            comunaSelect.innerHTML = '<option value="" disabled selected>Seleccione una comuna</option>';

            if (comunas.length === 0) {
                 comunaSelect.innerHTML += '<option value="" disabled>No hay comunas disponibles</option>';
            } else {
                comunas.forEach(comuna => {
                    const option = document.createElement('option');
                    // IMPORTANTE: El valor debe ser el ID de la comuna (es la PK en MySQL)
                    option.value = comuna.id; 
                    option.textContent = comuna.nombre;
                    comunaSelect.appendChild(option);
                });
            }
            
        } catch (error) {
            console.error("Error al cargar comunas:", error);
            comunaSelect.innerHTML = '<option value="" disabled selected>Error al cargar comunas</option>';
        } finally {
            comunaSelect.disabled = false;
        }
    };
    
    // 1. Eliminar la inicialización de datos locales (ya no se usa)
    // let region_comuna = {...};
    // const poblarRegiones = () => {...};
    // poblarRegiones();
    
    // 2. Modificar el Listener de Región para usar la función AJAX
    regionSelect.addEventListener('change', (event) => {
        const regionIdSeleccionada = event.target.value;
        cargarComunas(regionIdSeleccionada);
    });

    // --- FIN LÓGICA DINÁMICA ---


    // Lógica para agregar nuevas fotos
    let fotoCount = 1;
    agregarFotoBtn.addEventListener('click', () => {
        if (fotoCount < 5) {
            const nuevoInput = document.createElement('input');
            nuevoInput.type = 'file';
            nuevoInput.name = 'foto[]';
            nuevoInput.required = true;
            fotosContainer.insertBefore(nuevoInput, agregarFotoBtn);
            fotoCount++;
        }
        if (fotoCount === 5) {
            agregarFotoBtn.style.display = 'none';
        }
    });
    

    // --- Funciones de validación individuales ---
    const validateSelect = (selectElement) => {
        return selectElement.value !== "";
    };

    const validateName = (name) => {
        const trimmedName = name.trim();
        const lengthValid = trimmedName.length >= 3 && trimmedName.length <= 200;
        return lengthValid;
    };

    const validateEmail = (email) => {
        const lengthValid = email.length > 0 && email.length <= 100;
        const formatValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        return lengthValid && formatValid;
    };

    const validatePhoneNumber = (phoneNumber) => {
        if (phoneNumber.trim() === "") return true;
        
        const cleanedDigits = phoneNumber.replace(/[^\d]/g, ''); 
        const lengthValid = cleanedDigits.length >= 8;

        const formatValid = /^\+?\d+([\s\.]\d+)*$/.test(phoneNumber);
        
        return lengthValid && formatValid;
    };
    
    // Esta función se usa para validar TODOS los campos de contacto dinámicos
    const validateContactUrl = (contact) => {
        const lengthValid = contact.length >= 4 && contact.length <= 50;
        return lengthValid;
    };
    
    const validateNumberField = (value, min) => {
        const num = parseInt(value);
        return !isNaN(num) && num >= min;
    };
    
    const validateDeliveryDate = (dateString) => {
        const fechaEntrega = new Date(dateString);
        if (isNaN(fechaEntrega.getTime())) return false; 
        
        const fechaActualMas3Horas = new Date();
        fechaActualMas3Horas.setHours(fechaActualMas3Horas.getHours() + 3);
        
        return fechaEntrega >= fechaActualMas3Horas;
    };

    const validatePhotos = (files) => {
        const fileInputs = Array.from(files).filter(input => input.type === 'file');
        let count = 0;
        
        // Contar cuántos inputs tienen un archivo seleccionado
        fileInputs.forEach(input => {
            if (input.files && input.files.length > 0) {
                count++;
            }
        });
        
        // La validación original revisa el número de elementos input[type="file"],
        // la modificamos ligeramente para asegurar que al menos uno tenga contenido.
        // Asumiendo que por defecto el formulario tiene 1 input requerido.
        return count >= 1 && fileInputs.length <= 5;
    };
    
    // --- Lógica para mostrar/generar inputs de contacto dinámicos ---
    contactSelect.addEventListener('change', (event) => {
         // Limpia el contenedor de inputs anteriores
         contactContainer.innerHTML = '';
        
         // Obtiene las opciones seleccionadas que tienen un valor (excluye el placeholder/disabled)
         const selectedOptions = Array.from(event.target.selectedOptions)
             .filter(option => option.value !== "");
        
         if (selectedOptions.length > 0) {
            
             selectedOptions.forEach(option => {
                 const contactName = option.textContent; 
                 const contactValue = option.value;     
                
                 // 1. Crear el contenedor (para manejar el salto de línea)
                 const inputWrapper = document.createElement('div');
                 inputWrapper.classList.add('dynamic-contact-input'); 
                 inputWrapper.style.marginBottom = '10px';
                 
                 // 2. Crear la etiqueta
                 const label = document.createElement('label');
                 // Si el valor es 'otra', usamos el texto ingresado en el input
                 const displayContactName = contactValue === 'otra' ? 'Otro Método' : contactName;
                 label.textContent = `ID/URL para ${displayContactName}: `;
                 label.htmlFor = `contacto-url-${contactValue}`;
                 
                 // 3. Crear el input
                 const input = document.createElement('input');
                 input.type = 'text';
                 input.id = `contacto-url-${contactValue}`;
                 // Nombre clave para que Flask lo reciba: usa el valor del select como clave del array
                 input.name = `${contactValue}`; 
                 input.placeholder = `Escribe el ID o URL para ${displayContactName}`;
                 input.required = true; 
                 input.minlength = 4;
                 input.maxlength = 50;
                
                 // 4. Agregar al contenedor principal
                 inputWrapper.appendChild(label);
                 inputWrapper.appendChild(input);
                 contactContainer.appendChild(inputWrapper);
             });

             // Muestra el contenedor principal
             contactContainer.style.display = 'block';

         } else {
             // Oculta el contenedor si no hay nada seleccionado
             contactContainer.style.display = 'none';
         }
    });


    // --- Función principal de validación ---
    const validateForm = () => {
        let invalidInputs = [];
        
        // Validaciones fijas
        if (!validateSelect(regionSelect)) {
            invalidInputs.push("Región");
        }
        if (!validateSelect(comunaSelect)) {
            invalidInputs.push("Comuna");
        }
        if (!validateName(nombreInput.value)) {
            invalidInputs.push("Nombre (3-200 caracteres)");
        }
        if (!validateEmail(emailInput.value)) {
            invalidInputs.push("Email");
        }
        if (!validatePhoneNumber(celularInput.value)) {
            invalidInputs.push("Número de Celular (Formato: +569.12345678 o similar, con 8 o más dígitos)");
        }
        
        

        // VALIDACIÓN DINÁMICA DE CONTACTOS
        const selectedContactOptions = Array.from(contactSelect.options)
            .filter(option => option.selected && option.value !== "");
            
        selectedContactOptions.forEach(option => {
            const inputId = `contacto-url-${option.value}`;
            const dynamicInput = document.getElementById(inputId);
            
            // Si el input existe, validamos su contenido
            if (dynamicInput) {
                const contactValue = dynamicInput.value.trim();
                if (!validateContactUrl(contactValue)) {
                    invalidInputs.push(`ID/URL para ${option.textContent} (4-50 caracteres, no puede estar vacío)`);
                }
            }
        });
        
        if (!validateSelect(tipoSelect)) {
            invalidInputs.push("Tipo de Mascota");
        }
        if (!validateNumberField(cantidadInput.value, 1)) {
            invalidInputs.push("Cantidad (número entero >= 1)");
        }
        if (!validateNumberField(edadInput.value, 1)) {
            invalidInputs.push("Edad (número entero >= 1)");
        }
        if (!validateSelect(unidadEdadSelect)) {
            invalidInputs.push("Unidad de la edad");
        }
        if (fechaEntregaInput.value && !validateDeliveryDate(fechaEntregaInput.value)) {
            invalidInputs.push("Fecha de entrega (debe ser mayor o igual a la actual + 3 horas)");
        }
        
        // Validar que haya al menos 1 foto
        const allFileInputs = document.querySelectorAll('input[type="file"]');
        if (!validatePhotos(allFileInputs)) {
            invalidInputs.push("Fotos (debe subir entre 1 y 5 fotos)");
        }

        return invalidInputs;
    };

    // Manejo del evento de envío del formulario
    formulario.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const errores = validateForm();
        
        if (errores.length > 0) {
            window.scroll(0,0);

            validations.innerHTML = `
            <h3>Campos inválidos</h3>
            <ul>${errores.map(e => `<li>${e}</li>`).join("")}</ul>
            `;

            validations.style.display = "block";
            validations.style.background = "#fff8e1";
            validations.style.border = "1px solid #ffb300";
            validations.style.color = "#795548";
            validations.style.padding = "25px";
            validations.style.marginBottom = "15px";
            validations.style.borderRadius = "6px";
            return;

        } else {
            // Si no hay errores, mostrar la confirmación y hacer el submit
            validations.style.display = "none";
            
            const confirmacion = window.confirm("¿Está seguro que desea agregar este aviso de adopción?");
            if (confirmacion) {
                // Si el usuario confirma, enviamos el formulario a la URL de Flask
                formulario.submit(); 
                
                // Nota: La redirección y mensaje de éxito ahora lo maneja Flask
                // después de insertar en la base de datos.
            }
        }
    });

    // Asegurar que, si el formulario está cargado con un valor de región, las comunas se carguen.
    if (regionSelect.value) {
        cargarComunas(regionSelect.value);
    }
});
