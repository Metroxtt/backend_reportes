from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Usuarios

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    if not correo or not contrasena:
        return jsonify({"msg": "correo y contrasena requeridos"}), 400

    # Buscar usuario
    usuario = Usuarios.query.filter_by(correo=correo).first()

    if not usuario:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    # Validar contraseña (sin hashing por ahora)
    if usuario.contrasena != contrasena:
        return jsonify({"msg": "Contraseña incorrecta"}), 401

    return jsonify({
        "id_usuario": usuario.id_usuario,
        "correo": usuario.correo,
        "id_tipo_usuario": usuario.id_tipo_usuario,
        "activo": usuario.activo
    }), 200
