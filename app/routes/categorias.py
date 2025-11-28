from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Prioridad, CategoriaReportes

bp = Blueprint('categorias', __name__)

# --- Rutas para Prioridad ---

@bp.route('/prioridades', methods=['GET'])
def listar_prioridades():
    """Obtiene todas las prioridades."""
    prioridades = Prioridad.query.all()
    resultado = [{"id_prioridad": p.id_prioridad, "nombre": p.nombre} for p in prioridades]
    return jsonify(resultado), 200

@bp.route('/prioridades', methods=['POST'])
def crear_prioridad():
    """Crea una nueva prioridad."""
    data = request.json
    if not data.get('nombre'):
        return jsonify({"msg": "'nombre' es requerido"}), 400
        
    nueva = Prioridad(nombre=data.get('nombre'))
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"id_prioridad": nueva.id_prioridad, "nombre": nueva.nombre}), 201

# --- Rutas para CategoriaReportes ---

@bp.route('/reportes', methods=['GET'])
def listar_categorias_reportes():
    """
    Obtiene categorías incluyendo el NOMBRE de la prioridad.
    """
    categorias = CategoriaReportes.query.all()
    resultado = []
    
    for c in categorias:
        # Obtenemos el nombre de la prioridad usando la relación (backref)
        nombre_prioridad = "Media" # Default
        if c.prioridad:
            nombre_prioridad = c.prioridad.nombre

        resultado.append({
            "id_categoria": c.id_categoria,
            "nombre": c.nombre,
            "descripcion": c.descripcion,
            # Enviamos el nombre para que el Frontend sepa pintar colores
            "prioridad": nombre_prioridad 
        })
        
    return jsonify(resultado), 200

@bp.route('/reportes', methods=['POST'])
def crear_categoria_reporte():
    """Crea una nueva categoría de reporte."""
    data = request.json
    if not data.get('nombre') or not data.get('id_prioridad'):
        return jsonify({"msg": "'nombre' y 'id_prioridad' son requeridos"}), 400

    nueva = CategoriaReportes(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        id_prioridad=data.get('id_prioridad')
    )
    try:
        db.session.add(nueva)
        db.session.commit()
        return jsonify({"id_categoria": nueva.id_categoria, "nombre": nueva.nombre}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al crear categoría: {str(e)}"}), 500