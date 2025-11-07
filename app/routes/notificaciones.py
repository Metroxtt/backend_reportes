from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import TipoNotificacion, Alertas

bp = Blueprint('notificaciones', __name__)

# --- Rutas para TipoNotificacion ---

@bp.route('/tipos', methods=['GET'])
def listar_tipos_notificacion():
    """Obtiene todos los tipos de notificación."""
    tipos = TipoNotificacion.query.all()
    resultado = [{"id_tipo_notificacion": t.id_tipo_notificacion, "nombre": t.nombre} for t in tipos]
    return jsonify(resultado), 200

@bp.route('/tipos', methods=['POST'])
def crear_tipo_notificacion():
    """Crea un nuevo tipo de notificación."""
    data = request.json
    if not data.get('nombre'):
        return jsonify({"msg": "'nombre' es requerido"}), 400
        
    nuevo = TipoNotificacion(nombre=data.get('nombre'))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"id_tipo_notificacion": nuevo.id_tipo_notificacion, "nombre": nuevo.nombre}), 201

# --- Rutas para Alertas ---

@bp.route('/alertas', methods=['GET'])
def listar_alertas():
    """Obtiene todas las alertas."""
    alertas = Alertas.query.all()
    resultado = []
    for a in alertas:
        resultado.append({
            "id_alerta": a.id_alerta,
            "titulo": a.titulo,
            "mensaje": a.mensaje,
            "fecha_emision": a.fecha_emision.isoformat(),
            "ubigeo_id": a.ubigeo_id,
            "id_tipo_notificacion": a.id_tipo_notificacion
        })
    return jsonify(resultado), 200

@bp.route('/alertas', methods=['POST'])
def crear_alerta():
    """Crea una nueva alerta."""
    data = request.json
    if not data.get('titulo') or not data.get('mensaje') or not data.get('id_tipo_notificacion'):
        return jsonify({"msg": "'titulo', 'mensaje' y 'id_tipo_notificacion' son requeridos"}), 400

    nueva = Alertas(
        titulo=data.get('titulo'),
        mensaje=data.get('mensaje'),
        ubigeo_id=data.get('ubigeo_id'),
        id_tipo_notificacion=data.get('id_tipo_notificacion')
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"id_alerta": nueva.id_alerta, "titulo": nueva.titulo}), 201
