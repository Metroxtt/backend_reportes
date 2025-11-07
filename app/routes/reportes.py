from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Reportes

bp = Blueprint('reportes', __name__)

@bp.route('/', methods=['GET'])
def listar_reportes():
    q = Reportes.query.all()
    res = []
    for r in q:
        res.append({
            "Id_Reporte": r.Id_Reporte,
            "Id_Usuario": r.Id_Usuario,
            "Id_Categoria": r.Id_Categoria,
            "Id_Estado": r.Id_Estado,
            "Ubigeo": r.IdDist,
            "Fecha_Reporte": r.Fecha_Reporte.isoformat()
        })
    return jsonify(res), 200

@bp.route('/', methods=['POST'])
def crear_reporte():
    data = request.json
    nuevo = Reportes(
        Id_Usuario = data.get('id_usuario'),
        Id_Categoria = data.get('id_categoria'),
        Id_Estado = data.get('id_estado', 1),
        IdDist = data.get('ubigeo'),
        Descripcion = data.get('descripcion'),
        Latitud = data.get('latitud'),
        Longitud = data.get('longitud'),
        Evidencia_URL = data.get('evidencia_url')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"Id_Reporte": nuevo.Id_Reporte}), 201
