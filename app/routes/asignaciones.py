from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Asignaciones

bp = Blueprint('asignaciones', __name__)

@bp.route('/', methods=['GET'])
def listar_asignaciones():
    """Obtiene todas las asignaciones."""
    asignaciones = Asignaciones.query.all()
    resultado = []
    for a in asignaciones:
        resultado.append({
            "id_asignacion": a.id_asignacion,
            "id_reporte": a.id_reporte,
            "id_municipalidad": a.id_municipalidad,
            "fecha_asignacion": a.fecha_asignacion.isoformat()
        })
    return jsonify(resultado), 200

@bp.route('/', methods=['POST'])
def crear_asignacion():
    """Crea una nueva asignación de reporte a municipalidad."""
    data = request.json
    if not data.get('id_reporte') or not data.get('id_municipalidad'):
        return jsonify({"msg": "'id_reporte' y 'id_municipalidad' son requeridos"}), 400

    nueva = Asignaciones(
        id_reporte=data.get('id_reporte'),
        id_municipalidad=data.get('id_municipalidad')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"id_asignacion": nueva.id_asignacion}), 201