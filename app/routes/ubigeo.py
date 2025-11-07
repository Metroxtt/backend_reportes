from flask import Blueprint, jsonify, request  # <-- Asegúrate de que 'request' esté importado
from ..extensions import db
from ..models import Ubigeo
from sqlalchemy.exc import IntegrityError # <-- Importante para manejar errores

bp = Blueprint('ubigeo', __name__)

@bp.route('/', methods=['GET'])
def listar_ubigeos():
    """Obtiene todos los registros de Ubigeo."""
    ubigeos = Ubigeo.query.all()
    resultado = []
    for u in ubigeos:
        resultado.append({
            "iddist": u.iddist,
            "nombdep": u.nombdep,
            "nombprov": u.nombprov,
            "nombdist": u.nombdist,
            "nom_capital": u.nom_capital,
            "region_natural": u.region_natural
        })
    return jsonify(resultado), 200

# ==========================================================
# ESTA ES LA RUTA PARA CREAR (POST)
# ==========================================================
@bp.route('/', methods=['POST'])
def crear_ubigeo():
    """Crea un nuevo registro de Ubigeo."""
    data = request.json
    
    iddist = data.get('iddist')
    nombdep = data.get('nombdep')
    nombprov = data.get('nombprov')
    nombdist = data.get('nombdist')

    # Validación de campos requeridos
    if not iddist or not nombdep or not nombprov or not nombdist:
        return jsonify({"msg": "Los campos 'iddist', 'nombdep', 'nombprov' y 'nombdist' son requeridos"}), 400

    # Crear la nueva instancia
    nuevo_ubigeo = Ubigeo(
        iddist=iddist,
        nombdep=nombdep,
        nombprov=nombprov,
        nombdist=nombdist,
        # Campos opcionales
        nom_capital=data.get('nom_capital'),
        cod_reg_nat=data.get('cod_reg_nat'),
        region_natural=data.get('region_natural')
    )
    
    try:
        db.session.add(nuevo_ubigeo)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # Manejar error de ID duplicado (Primary Key)
        if "violates unique constraint" in str(e):
             return jsonify({"msg": f"Error: El iddist '{iddist}' ya existe."}), 409
        # Otro error de base de datos
        return jsonify({"msg": f"Error de base de datos: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Un error ocurrió: {str(e)}"}), 500

    # Si todo salió bien
    return jsonify({"iddist": nuevo_ubigeo.iddist, "msg": "Ubigeo creado exitosamente"}), 201
# ==========================================================
# FIN DE LA RUTA POST
# ==========================================================

@bp.route('/<string:iddist>', methods=['GET'])
def obtener_ubigeo_por_id(iddist):
    """Obtiene un registro de Ubigeo por su ID."""
    u = Ubigeo.query.get(iddist)
    if not u:
        return jsonify({"msg": "Ubigeo no encontrado"}), 404
        
    return jsonify({
        "iddist": u.iddist,
        "nombdep": u.nombdep,
        "nombprov": u.nombprov,
        "nombdist": u.nombdist
    }), 200
