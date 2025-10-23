import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, timezone # <-- Aseguramos la importación de timezone
from app.utils.validations import validar_datos_aviso
from sqlalchemy import func, extract, desc  # Importamos extract y desc para consultas SQL

# Importación de la base de datos y modelos 
from app.database.db import db, Region, Comuna, AvisoAdopcion, Foto, ContactarPor, Comentario # Asegúrate de que Comentario esté importado
# Directorio donde se guardarán las imágenes subidas
# Se usa el directorio 'static/uploads' relativo a la ubicación del archivo __init__.py
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Constantes de configuración (Ajustar para tu base de datos MySQL)
DB_USER = 'cc5002'
DB_PASSWORD = 'programacionweb'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'tarea2'

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos
    # CAMBIO: Usamos PyMySQL como driver para asegurar compatibilidad
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Clave secreta para mensajes flash y sesiones (OBLIGATORIO en Flask)
    app.config['SECRET_KEY'] = 'una_clave_secreta_muy_larga_y_dificil'
    
    # Límite de tamaño de archivo (opcional, 16MB)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
    
    # Inicializa SQLAlchemy con la aplicación Flask
    db.init_app(app)

    # Definición del Blueprint (main)
    # CRÍTICO: El nombre del endpoint estático para el blueprint 'main' es 'main.static'
    main = Blueprint('main', __name__, static_folder='static')

    # --- Funciones de Utilidad ---
    
    def inicializar_db_y_precargar_datos(app):
        """Precarga 5 Avisos de Adopción si la tabla está vacía, asumiendo que las tablas y Comunas ya fueron cargadas por archivos SQL."""
        with app.app_context():
            try:
                print(">> Verificación de conexión a DB exitosa. Tablas asumidas como creadas.")

                # 1. Obtener referencias de comunas para la precarga de avisos
                comuna_lo_barnechea = Comuna.query.filter_by(nombre="Lo Barnechea").first()
                comuna_penalolen = Comuna.query.filter_by(nombre="Peñalolén").first()
                comuna_colina = Comuna.query.filter_by(nombre="Colina").first()
                comuna_estacion_central = Comuna.query.filter_by(nombre="Estacion Central").first()
                comuna_santiago = Comuna.query.filter_by(nombre="Santiago").first()
                
                # Verificación de seguridad antes de la precarga de avisos
                if any(c is None for c in [comuna_lo_barnechea, comuna_penalolen, comuna_colina, comuna_estacion_central, comuna_santiago]):
                    print(">> ADVERTENCIA: Faltan comunas en la base de datos (e.g., 'Lo Barnechea'). La precarga de avisos se omite.")
                    return

                # 2. Precargar 5 Avisos de Adopción (solo si la tabla está vacía)
                if AvisoAdopcion.query.count() == 0:
                    print(">> Precargando 5 avisos de adopción...")
                    
                    # Usando los nombres de fotos reales subidos:
                    # NOMBRES CORREGIDOS SEGÚN LO PROPORCIONADO POR EL USUARIO
                    avisos_data = [
                        {
                            "comuna": comuna_santiago, "sector": "Barrio Universitario", "nombre": "Camila Soto", "email": "camila.soto@ejemplo.com", "celular": "+56 9 5652 5155", 
                            "tipo": "gato", "cantidad": 1, "edad": 6, "unidad_medida": "m", 
                            "fecha_entrega": datetime.now() + timedelta(days=7), "descripcion": "Gatita siamés muy cariñosa, ideal para departamento.",
                            "fotos": ["siamese-cat.jpg"], "contacto": {"metodo": "whatsapp", "id": "+56956525155"},
                            "fecha_ingreso_offset": 5 # Días atrás
                        },
                        {
                            "comuna": comuna_penalolen, "sector": "Lo Hermida", "nombre": "Andrés Pizarro", "email": "andres.pizarro@ejemplo.com", "celular": "+56 9 1234 5678", 
                            "tipo": "perro", "cantidad": 2, "edad": 2, "unidad_medida": "a", 
                            "fecha_entrega": datetime.now() + timedelta(days=10), "descripcion": "Dos huskies siberianos, muy juguetones. Necesitan patio grande.",
                            "fotos": ["red-siberian-husky-portrait.jpg"], "contacto": {"metodo": "telegram", "id": "@andrespizarro"},
                            "fecha_ingreso_offset": 12 # Días atrás
                        },
                        {
                            "comuna": comuna_lo_barnechea, "sector": "La Dehesa", "nombre": "Valentina Díaz", "email": "valentina.diaz@ejemplo.com", "celular": "+56 9 9876 5432", 
                            "tipo": "perro", "cantidad": 2, "edad": 1, "unidad_medida": "a", 
                            "fecha_entrega": datetime.now() + timedelta(days=5), "descripcion": "Cachorros Boyero de Berna, amigables con niños y otras mascotas. Adoptar juntos si es posible.",
                            "fotos": ["boyer_de_berna_0.jpg"], "contacto": {"metodo": "X", "id": "@valediaz"},
                            "fecha_ingreso_offset": 35 # Días atrás (mes anterior)
                        },
                        {
                            "comuna": comuna_estacion_central, "sector": "Villa Las Parcelas", "nombre": "Javier Roa", "email": "javier.roa@ejemplo.com", "celular": "+56 9 5555 4444", 
                            "tipo": "gato", "cantidad": 1, "edad": 3, "unidad_medida": "m", 
                            "fecha_entrega": datetime.now() + timedelta(days=15), "descripcion": "Gatita carey rescatada, es un poco tímida al principio, pero muy leal.",
                            "fotos": ["tortoiseshell-sadie.jpg"], "contacto": {"metodo": "whatsapp", "id": "+56955554444"},
                            "fecha_ingreso_offset": 31 # Días atrás (mes anterior)
                        },
                        {
                            "comuna": comuna_colina, "sector": "Chicureo", "nombre": "Sofía Morales", "email": "sofia.morales@ejemplo.com", "celular": "+56 9 7777 8888", 
                            "tipo": "perro", "cantidad": 1, "edad": 3, "unidad_medida": "a", 
                            "fecha_entrega": datetime.now() + timedelta(days=2), "descripcion": "Perro Pastor Suizo. Ideal para guardia y compañía, muy obediente.",
                            # CORRECCIÓN: El nombre de archivo ahora coincide con el proporcionado:
                            "fotos": ["het-hondenplein-01-de-zwitserse-wi.jpg"], 
                            "contacto": {"metodo": "otra", "id": "www.sofiamorales.cl/contacto"},
                            "fecha_ingreso_offset": 65 # Días atrás (hace dos meses)
                        },
                    ]
                    
                    ruta_base = "uploads" # Carpeta dentro de static/
                    
                    for i, data in enumerate(avisos_data):
                        # 1. Crear Aviso
                        aviso = AvisoAdopcion(
                            comuna_id=data["comuna"].id,
                            sector=data["sector"],
                            nombre=data["nombre"],
                            email=data["email"],
                            celular=data["celular"],
                            tipo=data["tipo"],
                            cantidad=data["cantidad"],
                            edad=data["edad"],
                            unidad_medida=data["unidad_medida"],
                            fecha_entrega=data["fecha_entrega"],
                            fecha_ingreso=datetime.now() - timedelta(days=data["fecha_ingreso_offset"]), # Usar offset
                            descripcion=data["descripcion"],
                        )
                        db.session.add(aviso)
                        db.session.flush()
                        
                        # 2. Agregar Fotos
                        for foto_nombre in data["fotos"]:
                            foto_path = os.path.join(UPLOAD_FOLDER, foto_nombre)
                            # Nota: En una simulación, no podemos asegurar que las fotos existan.
                            # Para fines de prueba de DB, la omitimos.
                            # if not os.path.exists(foto_path):
                            #     print(f">> Atención: La imagen de precarga '{foto_nombre}' DEBE existir en static/uploads. Saltando foto.")
                            #     continue
                                
                            # Ruta guardada en DB: 'uploads/nombre_archivo.jpg'
                            ruta_relativa_db = os.path.join(ruta_base, foto_nombre)
                            
                            foto = Foto(actividad_id=aviso.id, ruta_archivo=ruta_relativa_db, nombre_archivo=foto_nombre)
                            db.session.add(foto)

                        # 3. Agregar Contacto
                        contacto_info = data["contacto"]
                        contacto = ContactarPor(
                            actividad_id=aviso.id,
                            nombre=contacto_info["metodo"], 
                            identificador=contacto_info["id"]
                        )
                        db.session.add(contacto)

                        # Agregar un comentario de prueba al primer aviso
                        if i == 0:
                            comentario_prueba = Comentario(
                                actividad_id=aviso.id,
                                nombre_usuario="Visitante Inicial",
                                texto="¡Qué gatito tan lindo! Espero encuentre pronto un hogar.",
                                fecha=datetime.now() - timedelta(minutes=30)
                            )
                            db.session.add(comentario_prueba)
                            
                    db.session.commit()
                    print(f">> Se precargaron {len(avisos_data)} avisos de adopción con éxito.")

                    
            except Exception as e:
                db.session.rollback()
                print(f"ERROR durante la inicialización de DB o precarga: {e}")


    # --- Rutas de la Aplicación ---
    
    @main.route('/')
    @main.route('/index.html')
    def index():
        # Obtener los últimos 5 avisos (ordenados por fecha descendente)
        avisos_raw = db.session.query(AvisoAdopcion, Comuna).join(Comuna).order_by(AvisoAdopcion.fecha_ingreso.desc()).limit(5).all()
        avisos = []
        for aviso, comuna in avisos_raw:
            primera_foto = Foto.query.filter_by(actividad_id=aviso.id).first()
            
            # --- CORRECCIÓN 1: Generación de URL de foto ---
            foto_url = url_for('main.static', filename='img/default.jpg') # Default
            if primera_foto and primera_foto.ruta_archivo:
                # Flask resolverá 'main.static' a '/static/...'
                foto_url = url_for('main.static', filename=primera_foto.ruta_archivo)
            # ---------------------------------------------
            
            avisos.append({
                'id': aviso.id,
                'fecha_ingreso': aviso.fecha_ingreso, 
                'tipo': aviso.tipo,
                'cantidad': aviso.cantidad,
                'edad': aviso.edad,
                'unidad_medida': aviso.unidad_medida,
                'comuna_nombre': comuna.nombre,
                # --- CORRECCIÓN 2: Incluir el sector ---
                'sector': aviso.sector, 
                # --------------------------------------
                'foto_principal': foto_url
            })
            
        return render_template('index.html', avisos=avisos)

    @main.route('/Listado.html')
    def listado():
        # Obtener todos los avisos
        avisos_raw = db.session.query(AvisoAdopcion, Comuna).join(Comuna).order_by(AvisoAdopcion.fecha_ingreso.desc()).all()
        avisos = []
        for aviso, comuna in avisos_raw:
            primera_foto = Foto.query.filter_by(actividad_id=aviso.id).first()
            
            # --- CORRECCIÓN 1: Generación de URL de foto ---
            foto_url = url_for('main.static', filename='img/default.jpg') # Default
            if primera_foto and primera_foto.ruta_archivo:
                # Flask resolverá 'main.static' a '/static/...'
                foto_url = url_for('main.static', filename=primera_foto.ruta_archivo)
            # ---------------------------------------------
            
            avisos.append({
                'id': aviso.id,
                'fecha_ingreso': aviso.fecha_ingreso,
                'tipo': aviso.tipo,
                'cantidad': aviso.cantidad,
                'edad': aviso.edad,
                'unidad_medida': aviso.unidad_medida,
                'comuna_nombre': comuna.nombre,
                # --- CORRECCIÓN 2: Incluir el sector ---
                'sector': aviso.sector,
                # --------------------------------------
                'foto_principal': foto_url
            })
        return render_template('Listado.html', avisos=avisos)

    # NUEVA RUTA: Ruta de API para obtener los detalles de un aviso por ID
    @main.route('/api/aviso/<int:actividad_id>')
    def api_detalle_aviso(actividad_id):
        """Devuelve todos los datos de un aviso en formato JSON."""
        # 1. Obtener Aviso Adopción
        aviso_raw = db.session.query(AvisoAdopcion, Comuna, Region)\
                              .join(Comuna, AvisoAdopcion.comuna_id == Comuna.id)\
                              .join(Region, Comuna.region_id == Region.id)\
                              .filter(AvisoAdopcion.id == actividad_id).first()
        
        if not aviso_raw:
            return jsonify({'error': 'Aviso no encontrado'}), 404

        aviso, comuna, region = aviso_raw
        
        # 2. Obtener Fotos y Contactos
        fotos_db = Foto.query.filter_by(actividad_id=aviso.id).all()
        contactos_db = ContactarPor.query.filter_by(actividad_id=aviso.id).all()

        # 3. Preparar los datos para JSON
        unidad_edad_txt = "años" if aviso.unidad_medida == 'a' else "meses"
        contacto_principal = contactos_db[0] if contactos_db else None
        
        # Necesitamos el contexto de la aplicación para resolver url_for en una API route
        with app.app_context():
            fotos_data = []
            for f in fotos_db:
                # Usar url_for dentro del contexto de app
                url = url_for('main.static', filename=f.ruta_archivo)
                fotos_data.append({'src': url, 'alt': f'Foto de {aviso.tipo}'})

        aviso_data = {
            'id': aviso.id,
            'fechaPublicacion': aviso.fecha_ingreso.strftime('%Y-%m-%d %H:%M'),
            'fechaEntrega': aviso.fecha_entrega.strftime('%Y-%m-%d %H:%M'),
            'region': region.nombre, 
            'comuna': comuna.nombre,
            'sector': aviso.sector, # Sector ya está incluido
            'cantidad': aviso.cantidad,
            'tipo': aviso.tipo.capitalize(), 
            'edad': f"{aviso.edad} {unidad_edad_txt}",
            'nombreContacto': aviso.nombre,
            'email': aviso.email, 
            'celular': aviso.celular, 
            'contactoPor': contacto_principal.nombre.capitalize() if contacto_principal else 'N/A',
            'descripcion': aviso.descripcion,
            'totalFotos': len(fotos_db),
            'fotos': fotos_data # Usamos las URLs generadas
        }
        
        return jsonify(aviso_data)

    # --- RUTA DETALLE DE AVISO (Para cargar Detalle.html)
    @main.route('/detalle/<int:aviso_id>')
    def detalle_aviso(aviso_id):
        """Renderiza la página de detalle, pasando el ID del aviso."""
        # Nota: La carga de datos específicos del aviso se hará vía API en el frontend
        return render_template('Detalle.html', aviso_id=aviso_id)


    @main.route('/Estadistica.html')
    def estadistica():
        return render_template('Estadistica.html')

    @main.route('/Adopcion.html', methods=['GET', 'POST'])
    def adopcion():
        regiones = Region.query.order_by(Region.nombre).all()

        if request.method == 'POST':
            
            archivos_fotos = request.files.getlist('foto[]')
            
            # 1. EJECUCIÓN DE LA VALIDACIÓN
            es_valido, errores = validar_datos_aviso(request.form, archivos_fotos)
            
            if not es_valido:
                return render_template('Adopcion.html', regiones=regiones)

            # Si es válido, procedemos a la inserción
            try:
                # 2. Extracción de Datos
                comuna_id = request.form.get('comuna')
                sector = request.form.get('sector', '')
                nombre_contacto = request.form.get('nombre')
                email_contacto = request.form.get('email')
                celular_contacto = request.form.get('celular', '')
                tipo_mascota = request.form.get('tipo')
                cantidad = int(request.form.get('cantidad'))
                edad = int(request.form.get('edad'))
                unidad_edad = request.form.get('unidad-edad')
                fecha_entrega = datetime.strptime(request.form.get('fecha-entrega'), '%Y-%m-%dT%H:%M')
                descripcion = request.form.get('descripcion', '')

                # 3. Creación del Aviso de Adopción
                nuevo_aviso = AvisoAdopcion(
                    comuna_id=comuna_id,
                    sector=sector,
                    nombre=nombre_contacto,
                    email=email_contacto,
                    celular=celular_contacto,
                    tipo=tipo_mascota,
                    cantidad=cantidad,
                    edad=edad,
                    unidad_medida=unidad_edad,
                    fecha_entrega=fecha_entrega,
                    fecha_ingreso=datetime.now(),
                    descripcion=descripcion,
                )
                db.session.add(nuevo_aviso)
                db.session.flush()

                # 4. Guardado de Fotos y archivos
                ruta_base = 'uploads' # Carpeta dentro de static/
                for archivo in archivos_fotos:
                    if archivo and archivo.filename != '':
                        filename = secure_filename(f"{nuevo_aviso.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{archivo.filename}")
                        # Ruta relativa que se guarda en la base de datos (ej: 'uploads/nombre_archivo.jpg')
                        ruta_relativa = os.path.join(ruta_base, filename)
                        # Ruta absoluta para guardar el archivo en el sistema
                        ruta_absoluta = os.path.join(UPLOAD_FOLDER, filename)
                        
                        archivo.save(ruta_absoluta)
                        
                        # Guardar en la tabla Foto (CRÍTICO: Usar actividad_id)
                        foto = Foto(actividad_id=nuevo_aviso.id, ruta_archivo=ruta_relativa, nombre_archivo=filename)
                        db.session.add(foto)

                # 5. Guardado de Métodos de Contacto
                metodos_seleccionados = request.form.getlist('contacto-por[]')
                
                for metodo_form in metodos_seleccionados:
                    identificador = request.form.get('otro-contacto-input') if metodo_form == 'otra' else request.form.get(metodo_form)
                    
                    if identificador:
                        contacto = ContactarPor(
                            actividad_id=nuevo_aviso.id, # CRÍTICO: Usar actividad_id
                            nombre=metodo_form, 
                            identificador=identificador
                        )
                        db.session.add(contacto)

                # 6. Commit de toda la transacción
                db.session.commit()
                flash('¡Aviso de adopción agregado con éxito!', 'success')
                return redirect(url_for('main.index'))

            except Exception as e:
                db.session.rollback()
                print(f"Error al guardar en la base de datos: {e}")
                flash('Error grave al guardar el aviso. Inténtelo de nuevo.', 'error')
                return render_template('Adopcion.html', regiones=regiones)


        # Carga del formulario GET
        return render_template('Adopcion.html', regiones=regiones)

    # --- Ruta AJAX para Comunas ---
    @main.route('/comunas/<int:region_id>')
    def get_comunas(region_id):
        """Devuelve una lista de comunas en formato JSON para una región dada."""
        comunas = Comuna.query.filter_by(region_id=region_id).order_by(Comuna.nombre).all()
        
        comunas_data = [{'id': c.id, 'nombre': c.nombre} for c in comunas]
        
        return jsonify(comunas_data)
        
    # ==============================================================================
    # RUTAS API (SERVICIOS DE DATOS JSON)
    # ==============================================================================

    # NUEVA RUTA API: Obtener Comentarios por ID de Aviso
    @main.route('/api/comentarios/<int:actividad_id>', methods=['GET'])
    def api_get_comentarios(actividad_id):
        """Devuelve la lista de comentarios para un aviso, ordenados por fecha descendente."""
        try:
            comentarios = Comentario.query.filter_by(actividad_id=actividad_id)\
                                        .order_by(Comentario.fecha.desc()).all()
            
            comentarios_data = []
            for c in comentarios:
                comentarios_data.append({
                    'nombre': c.nombre_usuario,
                    'texto': c.texto,
                    # Formato para mostrar: 'dd/mm/yyyy hh:mm'
                    'fecha': c.fecha.strftime('%d/%m/%Y %H:%M') 
                })
            
            return jsonify(comentarios_data)

        except Exception as e:
            print(f"Error al obtener comentarios: {e}")
            return jsonify({'error': 'Error al cargar los comentarios'}), 500

    # NUEVA RUTA API: Guardar un Comentario
    @main.route('/api/comentarios/<int:actividad_id>', methods=['POST'])
    def api_post_comentario(actividad_id):
        """Recibe datos JSON para crear un nuevo comentario."""
        # Se espera que el body sea JSON: {"nombre": "...", "comentario": "..."}
        data = request.get_json() 
        
        if not data or not data.get('nombre') or not data.get('comentario'):
            return jsonify({'error': 'Faltan datos (nombre o comentario)'}), 400

        nombre_usuario = data['nombre']
        texto_comentario = data['comentario']

        try:
            # 1. Validar que el aviso exista (opcional pero buena práctica)
            aviso_existe = AvisoAdopcion.query.filter_by(id=actividad_id).first()
            if not aviso_existe:
                return jsonify({'error': 'El aviso no existe'}), 404

            # 2. Crear y guardar el comentario
            nuevo_comentario = Comentario(
                actividad_id=actividad_id,
                nombre_usuario=nombre_usuario,
                texto=texto_comentario,
                fecha=datetime.now()
            )
            db.session.add(nuevo_comentario)
            db.session.commit()

            # 3. Devolver el comentario recién creado para que el frontend lo agregue a la lista
            return jsonify({
                'nombre': nuevo_comentario.nombre_usuario,
                'texto': nuevo_comentario.texto,
                'fecha': nuevo_comentario.fecha.strftime('%d/%m/%Y %H:%M')
            }), 201 # 201 Created

        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar el nuevo comentario: {e}")
            return jsonify({'error': 'Error interno al guardar el comentario'}), 500


    @main.route('/api/stats/avisos_por_dia', methods=['GET'])
    def avisos_por_dia():
        """
        Retorna la cantidad de avisos de adopción agrupados por fecha de ingreso.
        Formato de salida: [[timestamp_ms, cantidad], ...]
        """
        try:
            # Consulta: Seleccionar Año, Mes, Día y contar.
            resultados = db.session.query(
                extract('year', AvisoAdopcion.fecha_ingreso).label('year'),
                extract('month', AvisoAdopcion.fecha_ingreso).label('month'),
                extract('day', AvisoAdopcion.fecha_ingreso).label('day'),
                func.count(AvisoAdopcion.id).label('count')
            ).group_by(
                'year', 'month', 'day'
            ).order_by(
                'year', 'month', 'day'
            ).all()
            
            # Formatear los datos para Highcharts
            datos_formateados = []
            for row in resultados:
                # 1. Crear el objeto datetime SIN información de hora y con timezone=UTC.
                try:
                    fecha_naive = datetime(int(row.year), int(row.month), int(row.day))
                except ValueError:
                    continue 

                # 2. Asignar zona horaria UTC (00:00:00) a la fecha, CRÍTICO para Highcharts
                fecha_utc = fecha_naive.replace(tzinfo=timezone.utc) 
                
                # 3. Convertir a timestamp UNIX en milisegundos y asegurar que es un entero
                timestamp_ms = int(fecha_utc.timestamp() * 1000) 
                
                datos_formateados.append([timestamp_ms, row.count])
                
            return jsonify(datos_formateados)

        except Exception as e:
            # Imprimimos el error, que es vital para la depuración
            print(f"Error CRÍTICO al obtener avisos_por_dia: {e}") 
            return jsonify([]) 


    @main.route('/api/stats/total_por_tipo', methods=['GET'])
    def total_por_tipo():
        """
        Retorna la cantidad total de avisos de adopción agrupados por tipo (perro/gato).
        Formato de salida (Highcharts Pie): [{"name": "perro", "y": 15}, ...]
        """
        try:
            # Consulta: Contar los avisos, agrupando por tipo (gato/perro).
            resultados = db.session.query(
                AvisoAdopcion.tipo,
                func.count(AvisoAdopcion.id)
            ).group_by(
                AvisoAdopcion.tipo
            ).all()
            
            # Formatear los datos para Highcharts Pie Chart
            datos_formateados = [
                {"name": tipo.capitalize(), "y": cantidad}
                for tipo, cantidad in resultados
            ]
                
            return jsonify(datos_formateados)

        except Exception as e:
            print(f"Error al obtener total_por_tipo: {e}")
            return jsonify({"error": "Error interno del servidor al consultar la base de datos"}), 500


    @main.route('/api/stats/mensual_por_tipo', methods=['GET'])
    def mensual_por_tipo():
        """
        Retorna la cantidad de avisos de adopción agrupados por mes y tipo (perro/gato).
        Formato de salida: {"categorias_x": [...], "gatos": [...], "perros": [...]}
        """
        meses_nombres = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        
        try:
            # Consulta: Agrupar por año, mes y tipo, y contar.
            # Usamos extract(year/month) para MySQL (funciona con SQLAlchemy).
            # Ordenamos por año y mes para la cronología.
            resultados_raw = db.session.query(
                extract('year', AvisoAdopcion.fecha_ingreso).label('year'),
                extract('month', AvisoAdopcion.fecha_ingreso).label('month'),
                AvisoAdopcion.tipo,
                func.count(AvisoAdopcion.id).label('count')
            ).group_by(
                'year', 'month', AvisoAdopcion.tipo
            ).order_by(
                'year', 'month'
            ).all()

            # Diccionario para almacenar los datos agrupados por mes (clave: Año-Mes)
            data_por_mes = {} 
            
            for row in resultados_raw:
                # Clave: "2023-10"
                clave_mes = f"{int(row.year)}-{int(row.month):02d}" 
                
                if clave_mes not in data_por_mes:
                    data_por_mes[clave_mes] = {
                        "categoria": f"{meses_nombres[int(row.month)-1]} {int(row.year)}",
                        "gato": 0,
                        "perro": 0
                    }
                
                # Asignar el conteo al tipo correspondiente
                if row.tipo == 'gato':
                    data_por_mes[clave_mes]["gato"] = row.count
                elif row.tipo == 'perro':
                    data_por_mes[clave_mes]["perro"] = row.count

            # Reorganizar los datos en el formato final para Highcharts
            categorias_x = [data['categoria'] for data in data_por_mes.values()]
            datos_gatos = [data['gato'] for data in data_por_mes.values()]
            datos_perros = [data['perro'] for data in data_por_mes.values()]
            
            datos_finales = {
                "categorias_x": categorias_x,
                "gatos": datos_gatos,
                "perros": datos_perros
            }
            
            return jsonify(datos_finales)

        except Exception as e:
            print(f"Error al obtener mensual_por_tipo: {e}")
            return jsonify({"error": "Error interno del servidor al consultar la base de datos"}), 500
            
    # --- Registro de Blueprint y Lógica de Inicialización ---
    app.register_blueprint(main)
    
    # Crea tablas y precarga datos al iniciar la aplicación (una sola vez)
    with app.app_context():
        # Aseguramos que la precarga de datos use el offset para tener datos en meses distintos
        inicializar_db_y_precargar_datos(app)
        
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
