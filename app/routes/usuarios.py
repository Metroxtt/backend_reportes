from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Usuarios, DatosUsuarios

bp = Blueprint('usuarios', __name__)

# ==========================================================
# RUTAS BÁSICAS (CRUD)
# ==========================================================

@bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = Usuarios.query.all()
    result = []
    for u in usuarios:
        # Intentamos obtener datos personales si existen
        nombre_completo = "Sin datos"
        telefono = ""
        if u.datos:
            nombre_completo = u.datos.nombre
            telefono = u.datos.telefono

        result.append({
            "id_usuario": u.id_usuario,
            "correo": u.correo,
            "nombre": nombre_completo,
            "telefono": telefono,
            "activo": u.activo,
            "fecha_registro": u.fecha_registro.isoformat()
        })
    return jsonify(result), 200


@bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.json
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    id_tipo = data.get('id_tipo_usuario', 1)

    if not correo or not contrasena:
        return jsonify({"msg": "correo y contrasena requeridos"}), 400

    # Crear usuario básico
    u = Usuarios(correo=correo, contrasena=contrasena, id_tipo_usuario=id_tipo)
    
    try:
        db.session.add(u)
        db.session.commit()
        return jsonify({"id_usuario": u.id_usuario, "msg": "Usuario creado"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al crear usuario: {str(e)}"}), 500


@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"msg": "pong desde backend actualizado"}), 200


# ==========================================================
# RUTAS DE PERFIL Y SEGURIDAD (NUEVAS)
# ==========================================================

@bp.route('/actualizar_perfil', methods=['PUT'])
def actualizar_perfil():
    """
    Actualiza el correo en la tabla 'usuarios' y 
    el nombre/teléfono en 'datos_usuarios'.
    """
    data = request.json
    id_usuario = data.get('id_usuario')
    
    if not id_usuario:
        return jsonify({"msg": "Falta id_usuario"}), 400

    # 1. Buscar el usuario principal
    usuario = Usuarios.query.get(id_usuario)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    try:
        # 2. Actualizar datos de la cuenta (correo)
        if 'email' in data:
            usuario.correo = data['email']

        # 3. Actualizar datos personales (nombre, apellido, telefono)
        # Concatenamos nombre y apellido porque la BD solo tiene campo 'nombre'
        nuevo_nombre = data.get('nombre', '')
        nuevo_apellido = data.get('apellido', '')
        nombre_completo = f"{nuevo_nombre} {nuevo_apellido}".strip()
        nuevo_telefono = data.get('telefono')

        # Buscamos si tiene registro en datos_usuarios
        # Nota: DatosUsuarios usa 'dni' como PK y 'id_usuario' como FK.
        # Buscamos por la relación FK.
        datos_personales = DatosUsuarios.query.filter_by(id_usuario=id_usuario).first()

        if datos_personales:
            if nombre_completo:
                datos_personales.nombre = nombre_completo
            if nuevo_telefono is not None:
                datos_personales.telefono = nuevo_telefono
        else:
            # Si no tiene datos personales (ej. registro rápido), 
            # NO podemos crearlos sin DNI porque es PK en tu modelo.
            # Por ahora solo actualizamos el correo y avisamos.
            print("Advertencia: El usuario no tiene tabla DatosUsuarios vinculada (falta DNI).")

        db.session.commit()
        return jsonify({"msg": "Perfil actualizado correctamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al actualizar: {str(e)}"}), 500


@bp.route('/cambiar_password', methods=['POST'])
def cambiar_password():
    """
    Verifica la contraseña actual y establece una nueva.
    """
    data = request.json
    id_usuario = data.get('id_usuario')
    password_actual = data.get('password_actual')
    password_nuevo = data.get('password_nuevo')

    if not id_usuario or not password_actual or not password_nuevo:
        return jsonify({"msg": "Faltan datos"}), 400

    usuario = Usuarios.query.get(id_usuario)
    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    # Verificar contraseña actual (Texto plano según tu auth.py)
    if usuario.contrasena != password_actual:
        return jsonify({"msg": "La contraseña actual es incorrecta"}), 401

    try:
        # Guardar nueva contraseña
        usuario.contrasena = password_nuevo
        db.session.commit()
        return jsonify({"msg": "Contraseña actualizada"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error interno: {str(e)}"}), 500
    



    # 🔥 NUEVA RUTA: Obtener perfil de un usuario específico con estadísticas
@bp.route('/<int:id_usuario>', methods=['GET'])
def obtener_perfil_usuario(id_usuario):
    # 1. Buscar usuario
    u = Usuarios.query.get(id_usuario)
    if not u:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    # 2. Obtener datos personales (si existen)
    nombre_completo = "Usuario Sin Nombre"
    telefono = ""
    dni = ""
    if u.datos:
        nombre_completo = u.datos.nombre
        telefono = u.datos.telefono
        dni = u.datos.dni

    # 3. Calcular estadísticas en tiempo real
    # Usamos la relación 'reportes' que definiste en el modelo Usuarios
    total = len(u.reportes)
    
    # Asumiendo IDs de estado: 1=Pendiente, 2=En Proceso, 3=Resuelto
    # Ajusta estos IDs según tu tabla 'estado_reportes' real
    pendientes = sum(1 for r in u.reportes if r.id_estado == 1)
    en_proceso = sum(1 for r in u.reportes if r.id_estado == 2)
    resueltos = sum(1 for r in u.reportes if r.id_estado == 3)

    return jsonify({
        "id": str(u.id_usuario),
        "nombre_completo": nombre_completo,
        "email": u.correo,
        "telefono": telefono,
        "dni": dni,
        "fecha_registro": u.fecha_registro.isoformat(),
        "tipo_usuario": "Ciudadano", # O puedes buscar u.tipo_usuario.nombre
        "estadisticas": {
            "total_reportes": total,
            "pendientes": pendientes,
            "en_proceso": en_proceso,
            "resueltos": resueltos
        }
    }), 200