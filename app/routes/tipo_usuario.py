from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import TipoUsuario

bp = Blueprint('tipo_usuario', __name__)

@bp.route('/', methods=['GET'])
def listar_tipos_usuario():
    """Obtiene todos los tipos de usuario."""
    tipos = TipoUsuario.query.all()
    resultado = []
    for t in tipos:
        resultado.append({
            "id_tipo_usuario": t.id_tipo_usuario,
            "nombre": t.nombre
        })
    return jsonify(resultado), 200

@bp.route('/', methods=['POST'])
def crear_tipo_usuario():
    """Crea un nuevo tipo de usuario."""
    data = request.json
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({"msg": "El campo 'nombre' es requerido"}), 400

    nuevo_tipo = TipoUsuario(nombre=nombre)
    db.session.add(nuevo_tipo)
    db.session.commit()

    return jsonify({"id_tipo_usuario": nuevo_tipo.id_tipo_usuario, "nombre": nuevo_tipo.nombre}), 201

