from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Municipalidades

bp = Blueprint('municipalidades', __name__)

@bp.route('/', methods=['GET'])
def listar_municipalidades():
    """Obtiene todas las municipalidades."""
    municipalidades = Municipalidades.query.all()
    resultado = []
    for m in municipalidades:
        resultado.append({
            "id_municipalidad": m.id_municipalidad,
            "nombre": m.nombre,
            "direccion": m.direccion,
            "contacto": m.contacto,
            "correo": m.correo,
            "ubigeo_id": m.ubigeo_id
        })
    return jsonify(resultado), 200

@bp.route('/', methods=['POST'])
def crear_municipalidad():
    """Crea una nueva municipalidad."""
    data = request.json
    if not data.get('nombre') or not data.get('ubigeo_id'):
        return jsonify({"msg": "'nombre' y 'ubigeo_id' son requeridos"}), 400

    nueva = Municipalidades(
        nombre=data.get('nombre'),
        direccion=data.get('direccion'),
        contacto=data.get('contacto'),
        correo=data.get('correo'),
        ubigeo_id=data.get('ubigeo_id')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"id_municipalidad": nueva.id_municipalidad, "nombre": nueva.nombre}), 201
