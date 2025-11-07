from flask import Flask
from .config import Config
from .extensions import db, migrate, cors, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    # Blueprints
    from .routes.usuarios import bp as usuarios_bp
    from .routes.reportes import bp as reportes_bp
    from .routes.tipo_usuario import bp as tipo_usuario_bp
    from .routes.datos_usuarios import bp as datos_usuarios_bp
    from .routes.ubigeo import bp as ubigeo_bp                 
    from .routes.categorias import bp as categorias_bp           
    from .routes.estados_reportes import bp as estado_reportes_bp  
    from .routes.municipalidades import bp as municipalidades_bp    
    from .routes.asignaciones import bp as asignaciones_bp        
    from .routes.notificaciones import bp as notificaciones_bp



    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    app.register_blueprint(reportes_bp, url_prefix='/api/reportes')
    app.register_blueprint(tipo_usuario_bp, url_prefix='/api/tipo_usuario')
    app.register_blueprint(datos_usuarios_bp, url_prefix='/api/datos_usuarios')
    app.register_blueprint(ubigeo_bp, url_prefix='/api/ubigeo')
    app.register_blueprint(categorias_bp, url_prefix='/api/categorias')
    app.register_blueprint(estado_reportes_bp, url_prefix='/api/estados_reportes')
    app.register_blueprint(municipalidades_bp, url_prefix='/api/municipalidades')
    app.register_blueprint(asignaciones_bp, url_prefix='/api/asignaciones')
    app.register_blueprint(notificaciones_bp, url_prefix='/api/notificaciones')



    @app.route('/')
    def index():
        return {"message": "API Reportes Ciudadanos alive"}

    return app