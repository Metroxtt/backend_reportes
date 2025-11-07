from .extensions import db
from datetime import datetime

# ==============================================================
# 1. TABLAS DE USUARIOS Y DATOS PERSONALES
# ==============================================================

class TipoUsuario(db.Model):
    __tablename__ = 'tipo_usuario'
    id_tipo_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    usuarios = db.relationship('Usuarios', backref='tipo_usuario')


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id_tipo_usuario'), nullable=False)

    datos = db.relationship('DatosUsuarios', backref='usuario', uselist=False)
    reportes = db.relationship('Reportes', backref='usuario')


class DatosUsuarios(db.Model):
    __tablename__ = 'datos_usuarios'
    dni = db.Column(db.String(8), primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(200))
    fecha_nacimiento = db.Column(db.Date)


# ==============================================================
# 2. TABLA UBIGEO
# ==============================================================

class Ubigeo(db.Model):
    __tablename__ = 'ubigeo'
    iddist = db.Column(db.String(6), primary_key=True)
    nombdep = db.Column(db.String(100), nullable=False)
    nombprov = db.Column(db.String(100), nullable=False)
    nombdist = db.Column(db.String(100), nullable=False)
    nom_capital = db.Column(db.String(100))
    cod_reg_nat = db.Column(db.String(10))
    region_natural = db.Column(db.String(50))


# ==============================================================
# 3. TABLAS DE PRIORIDAD Y CATEGORÍAS
# ==============================================================

class Prioridad(db.Model):
    __tablename__ = 'prioridad'
    id_prioridad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    categorias = db.relationship('CategoriaReportes', backref='prioridad')


class CategoriaReportes(db.Model):
    __tablename__ = 'categoria_reportes'
    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    id_prioridad = db.Column(db.Integer, db.ForeignKey('prioridad.id_prioridad'), nullable=False)
    reportes = db.relationship('Reportes', backref='categoria')


# ==============================================================
# 4. TABLAS DE ESTADOS Y REPORTES
# ==============================================================

class EstadoReportes(db.Model):
    __tablename__ = 'estado_reportes'
    id_estado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    reportes = db.relationship('Reportes', backref='estado')


class Reportes(db.Model):
    __tablename__ = 'reportes'
    id_reporte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria_reportes.id_categoria'), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estado_reportes.id_estado'), nullable=False)
    ubigeo_id = db.Column(db.String(6), db.ForeignKey('ubigeo.iddist'), nullable=False)
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)
    descripcion = db.Column(db.String(455))
    evidencia_url = db.Column(db.String(255))
    latitud = db.Column(db.Numeric(10, 7))
    longitud = db.Column(db.Numeric(10, 7))

    historial = db.relationship('HistorialEstados', backref='reporte')
    asignaciones = db.relationship('Asignaciones', backref='reporte')


# ==============================================================
# 5. HISTORIAL DE ESTADOS
# ==============================================================

class HistorialEstados(db.Model):
    __tablename__ = 'historial_estados'
    id_historial = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_reporte = db.Column(db.Integer, db.ForeignKey('reportes.id_reporte'), nullable=False)
    estado_anterior = db.Column(db.Integer, db.ForeignKey('estado_reportes.id_estado'))
    estado_nuevo = db.Column(db.Integer, db.ForeignKey('estado_reportes.id_estado'), nullable=False)
    fecha_cambio = db.Column(db.DateTime, default=datetime.utcnow)
    observacion = db.Column(db.String(455))


# ==============================================================
# 6. MUNICIPALIDADES
# ==============================================================

class Municipalidades(db.Model):
    __tablename__ = 'municipalidades'
    id_municipalidad = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(200))
    contacto = db.Column(db.String(15))
    correo = db.Column(db.String(100))
    ubigeo_id = db.Column(db.String(6), db.ForeignKey('ubigeo.iddist'), nullable=False)

    asignaciones = db.relationship('Asignaciones', backref='municipalidad')


# ==============================================================
# 7. ASIGNACIONES
# ==============================================================

class Asignaciones(db.Model):
    __tablename__ = 'asignaciones'
    id_asignacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_reporte = db.Column(db.Integer, db.ForeignKey('reportes.id_reporte'), nullable=False)
    id_municipalidad = db.Column(db.Integer, db.ForeignKey('municipalidades.id_municipalidad'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)


# ==============================================================
# 8. ALERTAS Y NOTIFICACIONES
# ==============================================================

class TipoNotificacion(db.Model):
    __tablename__ = 'tipo_notificacion'
    id_tipo_notificacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    alertas = db.relationship('Alertas', backref='tipo_notificacion')


class Alertas(db.Model):
    __tablename__ = 'alertas'
    id_alerta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_emision = db.Column(db.DateTime, default=datetime.utcnow)
    ubigeo_id = db.Column(db.String(6), db.ForeignKey('ubigeo.iddist'))
    id_tipo_notificacion = db.Column(db.Integer, db.ForeignKey('tipo_notificacion.id_tipo_notificacion'), nullable=False)
