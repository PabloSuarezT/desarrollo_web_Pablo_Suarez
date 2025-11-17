import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, timezone 
from app.utils.validations import validar_datos_aviso, validar_datos_comentario
from sqlalchemy import func, extract, desc 

# Importación de la base de datos y modelos 
from app.database.db import db, Region, Comuna, AvisoAdopcion, Foto, ContactarPor, Comentario 
# Directorio donde se guardarán las imágenes subidas
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
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Clave secreta para mensajes flash y sesiones (OBLIGATORIO en Flask)
    app.config['SECRET_KEY'] = 'una_clave_secreta_muy_larga_y_dificil'
    
    # Límite de tamaño de archivo (opcional, 16MB)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
    
    # Inicializa SQLAlchemy con la aplicación Flask
    db.init_app(app)

    # Definición del Blueprint (main)
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
                    
                    avisos_data = [
                        {
                            "comuna": comuna_santiago, "sector": "Barrio Universitario", "nombre": "Camila Soto", "email": "camila.soto@ejemplo.com", "celular": "+56 9 5652 5155", 
                            "tipo": "gato", "cantidad": 1, "edad": 6, "unidad_medida": "m", 
                            "fecha_entrega": datetime.now() + timedelta(days=7), "descripcion": "Gatita siamés muy cariñosa, ideal para departamento.",
                            "contactos": [{"metodo": "whatsapp", "id": "+56956525155"}], 
                            "fotos": ["siamese-cat.jpg"],
                            "fecha_ingreso_offset": 5 
                        },
                        {
                            "comuna": comuna_penalolen, "sector": "Lo Hermida", "nombre": "Andrés Pizarro", "email": "andres.pizarro@ejemplo.com", "celular": "+56 9 1234 5678", 
                            "tipo": "perro", "cantidad": 2, "edad": 2, "unidad_medida": "a", 
                            "fecha_entrega": datetime.now() + timedelta(days=10), "descripcion": "Huskie siberiano, muy jugueton. Necesita patio grande.",
                            "contactos": [{"metodo": "telegram", "id": "@andrespizarro"}],
                            "fotos": ["red-siberian-husky-portrait.jpg"], 
                            "fecha_ingreso_offset": 12 
                        },
                        {
                            "comuna": comuna_lo_barnechea, "sector": "La Dehesa", "nombre": "Valentina Díaz", "email": "valentina.diaz@ejemplo.com", "celular": "+56 9 9876 5432", 
                            "tipo": "perro", "cantidad": 2, "edad": 1, "unidad_medida": "a", 
                            "fecha_entrega": datetime.now() + timedelta(days=5), "descripcion": "Boyeros de Berna, amigables con niños y otras mascotas. Adoptar juntos si es posible.",
                            "contactos": [{"metodo": "X", "id": "@valediaz"}],
                            "fotos": ["boyer_de_berna_0.jpg"], 
                            "fecha_ingreso_offset": 35 
                        },
                        {
                            "comuna": comuna_estacion_central, "sector": "Villa Las Parcelas", "nombre": "Javier Roa", "email": "javier.roa@ejemplo.com", "celular": "+56 9 5555 4444", 
                            "tipo": "gato", "cantidad": 1, "edad": 3, "unidad_medida": "m", 
                            "fecha_entrega": datetime.now() + timedelta(days=15), "descripcion": "Gatita carey rescatada, es un poco tímida al principio, pero muy leal.",
                            "contactos": [{"metodo": "whatsapp", "id": "+56955554444"}],
                            "fotos": ["tortoiseshell-sadie.jpg"], 
                            "fecha_ingreso_offset": 31 
                        },
                        {
                            "comuna": comuna_colina, "sector": "Chicureo", "nombre": "Sofía Morales", "email": "sofia.morales@ejemplo.com", "celular": "+56 9 7777 8888", 
                            "tipo": "perro", "cantidad": 1, "edad": 3, "unidad_medida": "a", 
                            "fecha_entrega": datetime.now() + timedelta(days=2), "descripcion": "Perro Pastor Suizo. Ideal para guardia y compañía, muy obediente.",
                            "contactos": [{"metodo": "otra", "id": "www.sofiamorales.cl/contacto"}],
                            "fotos": ["het-hondenplein-01-de-zwitserse-wi.jpg"], 
                            "fecha_ingreso_offset": 65 
                        },
                    ]
                    
                    ruta_base = "uploads" 
                    
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
                            fecha_ingreso=datetime.now() - timedelta(days=data["fecha_ingreso_offset"]), 
                            descripcion=data["descripcion"],
                        )
                        db.session.add(aviso)
                        db.session.flush()
                        
                        # 2. Agregar Fotos
                        for foto_nombre in data["fotos"]:
                            ruta_relativa_db = os.path.join(ruta_base, foto_nombre)
                            foto = Foto(actividad_id=aviso.id, ruta_archivo=ruta_relativa_db, nombre_archivo=foto_nombre)
                            db.session.add(foto)

                        # 3. Agregar Contacto (USANDO CONTACTOS COMO LISTA PARA MULTIPLES)
                        for contacto_info in data["contactos"]:
                            contacto = ContactarPor(
                                actividad_id=aviso.id,
                                nombre=contacto_info["metodo"], 
                                identificador=contacto_info["id"]
                            )
                            db.session.add(contacto)

                        # Agregar un comentario de prueba al primer aviso
                        if i == 0:
                            comentario_prueba = Comentario(
                                aviso_id=aviso.id,
                                nombre="Visitante Inicial",
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
            
            # --- Generación de URL de foto ---
            foto_url = url_for('main.static', filename='img/default.jpg') # Default
            if primera_foto and primera_foto.ruta_archivo:
                foto_url = url_for('main.static', filename=primera_foto.ruta_archivo)
            
            avisos.append({
                'id': aviso.id,
                'fecha_ingreso': aviso.fecha_ingreso, 
                'tipo': aviso.tipo,
                'cantidad': aviso.cantidad,
                'edad': aviso.edad,
                'unidad_medida': aviso.unidad_medida,
                'comuna_nombre': comuna.nombre,
                'sector': aviso.sector, 
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
            
            # --- Generación de URL de foto ---
            foto_url = url_for('main.static', filename='img/default.jpg') # Default
            if primera_foto and primera_foto.ruta_archivo:
                foto_url = url_for('main.static', filename=primera_foto.ruta_archivo)
            
            avisos.append({
                'id': aviso.id,
                'fecha_ingreso': aviso.fecha_ingreso,
                'tipo': aviso.tipo,
                'cantidad': aviso.cantidad,
                'edad': aviso.edad,
                'unidad_medida': aviso.unidad_medida,
                'comuna_nombre': comuna.nombre,
                'sector': aviso.sector,
                'foto_principal': foto_url
            })
        return render_template('Listado.html', avisos=avisos)

    # RUTA API: Obtener los detalles de un aviso por ID (VERIFICADA Y ROBUSTA)
    @main.route('/api/aviso/<int:actividad_id>')
    def api_detalle_aviso(actividad_id):
        """Devuelve todos los datos de un aviso en formato JSON, incluyendo TODOS los contactos."""
        try:
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
            
            # Procesamos la lista completa de contactos
            contactos_data = []
            for c in contactos_db:
                contactos_data.append({
                    'metodo': c.nombre.capitalize(),
                    'identificador': c.identificador
                })

            # CRÍTICO: Aseguramos que se devuelve un primer contacto por compatibilidad
            contacto_principal = contactos_data[0] if contactos_data else {'metodo': 'N/A', 'identificador': 'N/A'}
            
            with app.app_context():
                fotos_data = []
                for f in fotos_db:
                    url = url_for('main.static', filename=f.ruta_archivo)
                    fotos_data.append({'src': url, 'alt': f'Foto de {aviso.tipo}'})

            aviso_data = {
                'id': aviso.id,
                'fechaPublicacion': aviso.fecha_ingreso.strftime('%Y-%m-%d %H:%M'),
                'fechaEntrega': aviso.fecha_entrega.strftime('%Y-%m-%d %H:%M'),
                'region': region.nombre, 
                'comuna': comuna.nombre,
                'sector': aviso.sector, 
                'cantidad': aviso.cantidad,
                'tipo': aviso.tipo.capitalize(), 
                'edad': f"{aviso.edad} {unidad_edad_txt}",
                'nombreContacto': aviso.nombre,
                'email': aviso.email, 
                'celular': aviso.celular, 
                
                # Devolvemos el primer contacto (para compatibilidad)
                'contactoPor': contacto_principal['metodo'],
                'identificadorContacto': contacto_principal['identificador'],
                
                # Devolvemos la lista completa de contactos (para la corrección)
                'contactosDetalle': contactos_data, 
                
                'descripcion': aviso.descripcion,
                'totalFotos': len(fotos_db),
                'fotos': fotos_data 
            }
            
            return jsonify(aviso_data)
        
        except Exception as e:
            # Esto captura errores de SQL o de conexión que no son 404 y ayuda a depurar
            print(f"ERROR CRÍTICO en api_detalle_aviso para ID {actividad_id}: {e}")
            return jsonify({'error': 'Error interno del servidor al obtener el detalle'}), 500

    @main.route('/Estadistica.html')
    def estadistica():
        return render_template('Estadistica.html')

    @main.route('/evaluation.html')
    def evaluation():
        return render_template('evaluation.html')

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
                ruta_base = 'uploads' 
                for archivo in archivos_fotos:
                    if archivo and archivo.filename != '':
                        filename = secure_filename(f"{nuevo_aviso.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{archivo.filename}")
                        ruta_relativa = os.path.join(ruta_base, filename)
                        ruta_absoluta = os.path.join(UPLOAD_FOLDER, filename)
                        
                        archivo.save(ruta_absoluta)
                        
                        foto = Foto(actividad_id=nuevo_aviso.id, ruta_archivo=ruta_relativa, nombre_archivo=filename)
                        db.session.add(foto)

                # 5. Guardado de Métodos de Contacto
                metodos_seleccionados = request.form.getlist('contacto-por[]')
                
                for metodo_form in metodos_seleccionados:
                    identificador = request.form.get(metodo_form) 
                    
                    if identificador: 
                        contacto = ContactarPor(
                            actividad_id=nuevo_aviso.id, 
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

    # Rutas de comentarios y estadísticas se mantienen sin cambios...
    @main.route('/api/comentarios/<int:actividad_id>', methods=['GET'])
    def api_get_comentarios(actividad_id):
        """Devuelve la lista de comentarios para un aviso, ordenados por fecha descendente."""
        try:
            comentarios = Comentario.query.filter_by(aviso_id=actividad_id)\
                                        .order_by(Comentario.fecha.desc()).all()
            
            comentarios_data = []
            for c in comentarios:
                comentarios_data.append({
                    'nombre': c.nombre,
                    'texto': c.texto,
                    'fecha': c.fecha.strftime('%d/%m/%Y %H:%M') 
                })
            
            return jsonify(comentarios_data)

        except Exception as e:
            print(f"Error al obtener comentarios: {e}")
            return jsonify({'error': 'Error al cargar los comentarios'}), 500

    @main.route('/api/comentarios/<int:actividad_id>', methods=['POST'])
    def api_post_comentario(actividad_id):
        """Recibe datos JSON para crear un nuevo comentario."""
        data = request.get_json() 
        
        if not data or not data.get('nombre') or not data.get('comentario'):
            return jsonify({'error': 'Faltan datos (nombre o comentario)'}), 400

        nombre_usuario = data['nombre']
        texto_comentario = data['comentario']

        try:
            aviso_existe = AvisoAdopcion.query.filter_by(id=actividad_id).first()
            if not aviso_existe:
                return jsonify({'error': 'El aviso no existe'}), 404

            nuevo_comentario = Comentario(
                aviso_id=actividad_id,
                nombre=nombre_usuario,
                texto=texto_comentario,
                fecha=datetime.now()
            )
            db.session.add(nuevo_comentario)
            db.session.commit()

            return jsonify({
                'nombre': nuevo_comentario.nombre,
                'texto': nuevo_comentario.texto,
                'fecha': nuevo_comentario.fecha.strftime('%d/%m/%Y %H:%M')
            }), 201 

        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar el nuevo comentario: {e}")
            return jsonify({'error': 'Error interno al guardar el comentario'}), 500

    @main.route('/api/stats/avisos_por_dia', methods=['GET'])
    def avisos_por_dia():
        """
        Retorna la cantidad de avisos de adopción agrupados por fecha de ingreso.
        """
        try:
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
            
            datos_formateados = []
            for row in resultados:
                try:
                    fecha_naive = datetime(int(row.year), int(row.month), int(row.day))
                except ValueError:
                    continue 

                fecha_utc = fecha_naive.replace(tzinfo=timezone.utc) 
                timestamp_ms = int(fecha_utc.timestamp() * 1000) 
                
                datos_formateados.append([timestamp_ms, row.count])
                
            return jsonify(datos_formateados)

        except Exception as e:
            print(f"Error CRÍTICO al obtener avisos_por_dia: {e}") 
            return jsonify([]) 


    @main.route('/api/stats/total_por_tipo', methods=['GET'])
    def total_por_tipo():
        """
        Retorna la cantidad total de avisos de adopción agrupados por tipo (perro/gato).
        """
        try:
            resultados = db.session.query(
                AvisoAdopcion.tipo,
                func.count(AvisoAdopcion.id)
            ).group_by(
                AvisoAdopcion.tipo
            ).all()
            
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
        """
        meses_nombres = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        
        try:
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

            data_por_mes = {} 
            
            for row in resultados_raw:
                clave_mes = f"{int(row.year)}-{int(row.month):02d}" 
                
                if clave_mes not in data_por_mes:
                    data_por_mes[clave_mes] = {
                        "categoria": f"{meses_nombres[int(row.month)-1]} {int(row.year)}",
                        "gato": 0,
                        "perro": 0
                    }
                
                if row.tipo == 'gato':
                    data_por_mes[clave_mes]["gato"] = row.count
                elif row.tipo == 'perro':
                    data_por_mes[clave_mes]["perro"] = row.count

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
    
    with app.app_context():
        inicializar_db_y_precargar_datos(app)
        
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
