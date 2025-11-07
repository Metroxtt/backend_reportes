from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import DatosUsuarios
from datetime import date

bp = Blueprint('datos_usuarios', __name__)

@bp.route('/', methods=['GET'])
def listar_datos_usuarios():
    """Obtiene todos los datos personales de los usuarios."""
    datos = DatosUsuarios.query.all()
    resultado = []
    for d in datos:
        resultado.append({
            "dni": d.dni,
            "id_usuario": d.id_usuario,
            "nombre": d.nombre,
            "telefono": d.telefono,
            "direccion": d.direccion,
            "fecha_nacimiento": d.fecha_nacimiento.isoformat() if d.fecha_nacimiento else None
        })
    return jsonify(resultado), 200

@bp.route('/', methods=['POST'])
def crear_datos_usuario():
    """Crea o actualiza los datos personales de un usuario."""
    data = request.json
    
    # DNI es la clave primaria
    dni = data.get('dni')
    if not dni:
        return jsonify({"msg": "El 'dni' es requerido"}), 400

    # Crear nueva instancia
    nuevos_datos = DatosUsuarios(
        dni=dni,
        id_usuario=data.get('id_usuario'),
        nombre=data.get('nombre'),
        telefono=data.get('telefono'),
        direccion=data.get('direccion')
    )
    
    # Manejar fecha
    fecha_nac_str = data.get('fecha_nacimiento')
    if fecha_nac_str:
        try:
            nuevos_datos.fecha_nacimiento = date.fromisoformat(fecha_nac_str)
        except ValueError:
            return jsonify({"msg": "Formato de fecha incorrecto. Usar YYYY-MM-DD"}), 400

    db.session.add(nuevos_datos)
    db.session.commit()

    return jsonify({"dni": nuevos_datos.dni, "id_usuario": nuevos_datos.id_usuario}), 201

