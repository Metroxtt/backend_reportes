from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from ..extensions import db
# Importamos todos los modelos necesarios para obtener los nombres reales
from ..models import Reportes, Ubigeo, Usuarios, DatosUsuarios, CategoriaReportes, Prioridad, EstadoReportes

bp = Blueprint('reportes', __name__)

@bp.route('/', methods=['GET'])
def listar_reportes():
    """
    Obtiene todos los reportes pero TRANSFORMA los IDs (FK) 
    en texto legible para que Flutter lo pueda mostrar.
    """
    try:
        # Ordenamos por fecha descendente (lo más nuevo primero)
        reportes = Reportes.query.order_by(Reportes.fecha_reporte.desc()).all()
        resultado = []

        for r in reportes:
            # 1. Obtener NOMBRE del Usuario
            # Navegamos: Reporte -> Usuario -> DatosUsuarios -> nombre
            nombre_usuario = "Usuario Desconocido"
            if r.usuario and r.usuario.datos:
                nombre_usuario = r.usuario.datos.nombre
            
            # 2. Obtener NOMBRE de la Categoría y Prioridad
            nombre_categoria = "General"
            nombre_prioridad = "Media"
            
            if r.categoria:
                nombre_categoria = r.categoria.nombre
                # La prioridad está dentro de la categoría
                if r.categoria.prioridad:
                    nombre_prioridad = r.categoria.prioridad.nombre

            # 3. Obtener UBICACIÓN (Distrito)
            # Como tu modelo Reportes no tiene relación directa definida con Ubigeo,
            # lo buscamos manualmente por el ID.
            ubicacion_texto = r.ubigeo_id # Fallback por si no se encuentra
            if r.ubigeo_id:
                ubigeo_obj = Ubigeo.query.get(r.ubigeo_id)
                if ubigeo_obj:
                    # Formato: "Distrito, Provincia"
                    ubicacion_texto = f"{ubigeo_obj.nombdist}, {ubigeo_obj.nombprov}"

            # 4. Generar TÍTULO
            # Como no tienes columna título, lo creamos dinámicamente
            titulo_generado = f"Reporte de {nombre_categoria}"

            # Construimos el JSON con las claves EXACTAS que tu Flutter espera
            item = {
                "id": str(r.id_reporte), # Flutter suele preferir Strings para IDs en listas
                "categoria": nombre_categoria,
                "titulo": titulo_generado, 
                "descripcion": r.descripcion,
                "ubicacion": ubicacion_texto,
                "estado": r.estado.nombre if r.estado else "Desconocido",
                "prioridad": nombre_prioridad,
                "fechaCreacion": r.fecha_reporte.isoformat(),
                "nombreUsuario": nombre_usuario,
                "tieneImagen": bool(r.evidencia_url),
                # Datos extra útiles si decides usarlos luego:
                "latitud": float(r.latitud) if r.latitud else None,
                "longitud": float(r.longitud) if r.longitud else None,
                "url_imagen": r.evidencia_url
            }
            resultado.append(item)

        return jsonify(resultado), 200

    except Exception as e:
        print(f"Error cargando reportes: {e}")
        return jsonify({"msg": "Error interno del servidor"}), 500


@bp.route('/', methods=['POST'])
def crear_reporte():
    """Crea un nuevo reporte."""
    data = request.json

    # Validación de campos requeridos
    id_usuario = data.get('id_usuario')
    id_categoria = data.get('id_categoria')
    ubigeo_id = data.get('ubigeo_id')

    # El estado por defecto será 1 (Pendiente) si no se envía
    id_estado = data.get('id_estado', 1) 

    if not id_usuario or not id_categoria or not ubigeo_id:
        return jsonify({"msg": "Faltan datos: 'id_usuario', 'id_categoria' y 'ubigeo_id' son obligatorios"}), 400

    nuevo_reporte = Reportes(
        id_usuario = id_usuario,
        id_categoria = id_categoria,
        id_estado = id_estado,
        ubigeo_id = ubigeo_id,
        descripcion = data.get('descripcion'),
        latitud = data.get('latitud'),
        longitud = data.get('longitud'),
        evidencia_url = data.get('evidencia_url')
    )
    
    try:
        db.session.add(nuevo_reporte)
        db.session.commit()
        return jsonify({"msg": "Reporte creado exitosamente", "id_reporte": nuevo_reporte.id_reporte}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"msg": f"Error de integridad (IDs no válidos): {str(e)}"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error inesperado: {str(e)}"}), 500