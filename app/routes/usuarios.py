from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Usuarios, DatosUsuarios

bp = Blueprint('usuarios', __name__)

@bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = Usuarios.query.all()
    result = []
    for u in usuarios:
        result.append({
            "id_usuario": u.id_usuario,
            "correo": u.correo,
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

    # 🔧 Aquí corregimos el uso de los nombres en minúsculas
    u = Usuarios(correo=correo, contrasena=contrasena, id_tipo_usuario=id_tipo)

    db.session.add(u)
    db.session.commit()

    return jsonify({"id_usuario": u.id_usuario}), 201

@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"msg": "pong desde backend actualizado"}), 200