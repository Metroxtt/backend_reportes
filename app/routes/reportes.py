from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Reportes
# Importar IntegrityError para manejar errores de FK
from sqlalchemy.exc import IntegrityError

bp = Blueprint('reportes', __name__)

@bp.route('/', methods=['GET'])
def listar_reportes():
    """Obtiene todos los reportes."""
    reportes = Reportes.query.all()
    resultado = []
    for r in reportes:
        resultado.append({
            "id_reporte": r.id_reporte,
            "id_usuario": r.id_usuario,
            "id_categoria": r.id_categoria,
            "id_estado": r.id_estado,
            "ubigeo_id": r.ubigeo_id,
            "fecha_reporte": r.fecha_reporte.isoformat(),
            "descripcion": r.descripcion
        })
    return jsonify(resultado), 200

@bp.route('/', methods=['POST'])
def crear_reporte():
    """Crea un nuevo reporte."""
    data = request.json

    # Campos requeridos (los 4 IDs)
    # ¡Asegúrate de que las llaves en tu JSON coincidan!
    id_usuario = data.get('id_usuario')
    id_categoria = data.get('id_categoria')
    ubigeo_id = data.get('ubigeo_id') # ¡CORREGIDO! (antes 'ubigeo')
    
    # El estado puede tener un default (ej. 1 = "Pendiente")
    id_estado = data.get('id_estado', 1) 

    if not id_usuario or not id_categoria or not ubigeo_id:
        return jsonify({"msg": "'id_usuario', 'id_categoria' y 'ubigeo_id' son requeridos"}), 400

    # ¡AQUÍ ESTÁ LA CORRECCIÓN!
    # Los argumentos (izquierda) deben coincidir con las columnas del Modelo (minúsculas)
    nuevo_reporte = Reportes(
        id_usuario = id_usuario,         # ¡CORREGIDO!
        id_categoria = id_categoria,   # ¡CORREGIDO!
        id_estado = id_estado,         # ¡CORREGIDO!
        ubigeo_id = ubigeo_id,         # ¡CORREGIDO!
        descripcion = data.get('descripcion'), # ¡CORREGIDO!
        latitud = data.get('latitud'),         # ¡CORREGIDO!
        longitud = data.get('longitud'),        # ¡CORREGIDO!
        evidencia_url = data.get('evidencia_url') # ¡CORREGIDO!
    )
    
    try:
        db.session.add(nuevo_reporte)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # Esto es por si un id_usuario, id_categoria, etc., no existe
        return jsonify({"msg": f"Error de llave foránea (ForeignKeyViolation): {str(e)}"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error inesperado: {str(e)}"}), 500

    # Si todo salió bien
    return jsonify({"id_reporte": nuevo_reporte.id_reporte}), 201