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

    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')
    app.register_blueprint(reportes_bp, url_prefix='/api/reportes')

    @app.route('/')
    def index():
        return {"message": "API Reportes Ciudadanos alive"}

    return app