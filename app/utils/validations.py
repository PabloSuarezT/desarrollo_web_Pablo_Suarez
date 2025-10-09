import re
from datetime import datetime
from flask import flash

# Expresiones regulares para validaciones complejas
# Formato de celular: +NNN.NNNNNNNN
CELULAR_REGEX = re.compile(r'^\+\d{3}\.\d{8,15}$') # Permite 8 a 15 dígitos después del punto

def validar_datos_aviso(formulario, archivos_fotos):
    """
    Valida todos los campos del formulario de adopción según las reglas de la Tarea 1.
    Retorna True si todas las validaciones pasan, y False en caso contrario.
    Usa flash() para almacenar los mensajes de error.
    """
    errores = {}

    # --- 1. Información del Lugar y Contacto ---
    
    # Comuna (obligatoria)
    comuna_id = formulario.get('comuna')
    if not comuna_id:
        errores['comuna'] = 'Debe seleccionar una comuna.'
        
    # Sector (opcional, largo máximo 100)
    sector = formulario.get('sector', '')
    if len(sector) > 100:
        errores['sector'] = 'El sector no debe superar los 100 caracteres.'
        
    # Nombre de contacto (obligatorio, min 3, max 200)
    nombre = formulario.get('nombre')
    if not nombre or len(nombre) < 3 or len(nombre) > 200:
        errores['nombre'] = 'El nombre es obligatorio y debe tener entre 3 y 200 caracteres.'
        
    # Email (obligatorio, formato email, max 100)
    email = formulario.get('email')
    if not email:
        errores['email'] = 'El email es obligatorio.'
    elif len(email) > 100:
        errores['email'] = 'El email no debe superar los 100 caracteres.'
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errores['email'] = 'El formato del email es inválido.'

    # Celular (opcional, formato +NNN.NNNNNNNN)
    celular = formulario.get('celular', '')
    if celular and not CELULAR_REGEX.match(celular):
        errores['celular'] = 'El formato del celular es inválido. Debe ser +NNN.NNNNNNNN.'

    # --- 2. Información de la Mascota ---
    
    # Tipo (obligatorio)
    tipo_mascota = formulario.get('tipo')
    if tipo_mascota not in ['perro', 'gato']:
        errores['tipo'] = 'Debe seleccionar un tipo de mascota válido (Perro o Gato).'
        
    # Cantidad (obligatorio, entero, min 1)
    try:
        cantidad = int(formulario.get('cantidad'))
        if cantidad < 1:
            errores['cantidad'] = 'La cantidad debe ser un número entero mayor o igual a 1.'
    except (ValueError, TypeError):
        errores['cantidad'] = 'La cantidad es obligatoria y debe ser un número entero.'
        
    # Edad (obligatorio, entero, min 1)
    try:
        edad = int(formulario.get('edad'))
        if edad < 1:
            errores['edad'] = 'La edad debe ser un número entero mayor o igual a 1.'
    except (ValueError, TypeError):
        errores['edad'] = 'La edad es obligatoria y debe ser un número entero.'
        
    # Unidad de edad (obligatorio)
    unidad_edad = formulario.get('unidad-edad')
    if unidad_edad not in ['m', 'a']: # Asumiendo 'm' para meses, 'a' para años
        errores['unidad-edad'] = 'Debe seleccionar una unidad de medida de edad.'

    # Fecha disponible para entrega (obligatorio, debe ser mayor o igual a fecha actual + 3 horas)
    fecha_entrega_str = formulario.get('fecha-entrega')
    if not fecha_entrega_str:
        errores['fecha-entrega'] = 'La fecha de entrega es obligatoria.'
    else:
        try:
            fecha_entrega = datetime.strptime(fecha_entrega_str, '%Y-%m-%dT%H:%M')
            fecha_minima = datetime.now() + timedelta(hours=3)
            
            if fecha_entrega < fecha_minima:
                errores['fecha-entrega'] = 'La fecha de entrega debe ser posterior a la fecha actual más 3 horas.'
        except ValueError:
            errores['fecha-entrega'] = 'Formato de fecha de entrega inválido.'

    # Descripción (opcional)
    # No hay validación de largo, ya que es un campo TEXT(500) en la DB.

    # --- 3. Métodos de Contacto ---
    metodos_seleccionados = formulario.getlist('contacto-por[]')
    
    # Máximo 5 métodos
    if len(metodos_seleccionados) > 5:
        errores['contacto-por'] = 'Solo se permiten hasta 5 métodos de contacto.'
        
    # Validar que si se seleccionó un método, el ID/identificador no esté vacío
    for metodo in metodos_seleccionados:
        identificador = formulario.get(metodo) # Tries to get the input value for the method
        if metodo == 'otra':
            identificador = formulario.get('otro-contacto-input')

        if identificador:
            if len(identificador) < 4 or len(identificador) > 50:
                 errores[f'contacto-{metodo}'] = f'El ID/URL de contacto ({metodo}) debe tener entre 4 y 50 caracteres.'
        elif metodo != 'otra':
             # Aquí podríamos ser más estrictos, pero el formulario a veces envía el checkbox sin el input
             pass # Si el identificador es None o vacío, la validación estricta depende del frontend

    # --- 4. Fotos (obligatorio, min 1, max 5) ---
    valid_files = [f for f in archivos_fotos if f and f.filename != '']
    
    if len(valid_files) == 0:
        errores['foto'] = 'Debe subir al menos una foto.'
    elif len(valid_files) > 5:
        errores['foto'] = 'Solo se permiten hasta 5 fotos.'
        
    # --- Manejo de Errores Final ---
    if errores:
        # Almacena todos los errores para mostrarlos en el template (o usa flash como fallback)
        for key, msg in errores.items():
            flash(f'{key.capitalize()}: {msg}', 'error')
        return False, errores
    
    return True, {}

# Necesario para el chequeo de fecha
from datetime import timedelta
