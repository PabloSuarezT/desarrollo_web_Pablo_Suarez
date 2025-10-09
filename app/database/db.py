from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Instancia de SQLAlchemy (no se inicializa aquí, sino en app.py)
db = SQLAlchemy()

# -- Models --

class Region(db.Model):
    __tablename__ = "region"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    
    # Relación inversa (backref='region' en Comuna)
    comunas = db.relationship('Comuna', backref='region', lazy=True)

    def __repr__(self):
        return f'<Region {self.nombre}>'

class Comuna(db.Model):
    __tablename__ = "comuna"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    
    # Foreign Key
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    
    # Relación inversa (backref='comuna' en AvisoAdopcion)
    avisos_adopcion = db.relationship('AvisoAdopcion', backref='comuna', lazy=True) 

    def __repr__(self):
        return f'<Comuna {self.nombre} (ID: {self.id})>'

class AvisoAdopcion(db.Model): 
    __tablename__ = "aviso_adopcion"

    id = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    comuna_id = db.Column(db.Integer, db.ForeignKey('comuna.id'), nullable=False)
    sector = db.Column(db.String(100), nullable=True)
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable= False)
    celular = db.Column(db.String(15), nullable=True)
    tipo = db.Column(db.Enum('gato','perro', name='tipo_mascota'), nullable=False) 
    cantidad = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    unidad_medida = db.Column(db.Enum('a','m', name='unidad_edad'), nullable=False) 
    fecha_entrega = db.Column(db.DateTime, nullable=False) 
    descripcion = db.Column(db.Text(500), nullable=True) 

    # Relaciones
    fotos = db.relationship('Foto', 
                             backref='aviso_adopcion', 
                             lazy=True, 
                             cascade="all, delete-orphan",
                             foreign_keys='Foto.actividad_id') 
                             
    contactos = db.relationship('ContactarPor', 
                                backref='aviso_adopcion', 
                                lazy=True, 
                                cascade="all, delete-orphan",
                                foreign_keys='ContactarPor.actividad_id') 
    
    def __repr__(self):
        return f"<AvisoAdopcion {self.nombre}>"


class Foto(db.Model):
    __tablename__ = 'foto'
    
    id = db.Column(db.Integer, primary_key=True)
    ruta_archivo = db.Column(db.String(300), nullable=False)
    nombre_archivo = db.Column(db.String(300), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)

    def __repr__(self):
        return f'<Foto {self.nombre_archivo}>'


class ContactarPor(db.Model):
    __tablename__ = 'contactar_por'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # CORRECCIÓN: Agregamos 'email' al ENUM para evitar el error de truncamiento en la precarga
    nombre = db.Column(db.Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra', 'email', name='tipo_contacto_enum'), nullable=False)
    
    identificador = db.Column(db.String(150), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)
    
    def __repr__(self):
        return f'<Contacto {self.nombre} - {self.identificador}>'