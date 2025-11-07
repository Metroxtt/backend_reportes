from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import EstadoReportes

bp = Blueprint('estados_reportes', __name__)

@bp.route('/', methods=['GET'])
def listar_estados():
    """Obtiene todos los estados de reportes."""
    estados = EstadoReportes.query.all()
    resultado = [{"id_estado": e.id_estado, "nombre": e.nombre} for e in estados]
    return jsonify(resultado), 200

@bp.route('/', methods=['POST'])
def crear_estado():
    """Crea un nuevo estado de reporte."""
    data = request.json
    if not data.get('nombre'):
        return jsonify({"msg": "'nombre' es requerido"}), 400
        
    nuevo = EstadoReportes(nombre=data.get('nombre'))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"id_estado": nuevo.id_estado, "nombre": nuevo.nombre}), 201
