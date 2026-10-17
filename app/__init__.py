import logging

from flask import Flask, jsonify

from .config import get_config
from .extensions import db, login_manager, migrate, register_blueprints


def create_app(config_object=None):
    app = Flask(__name__)
    config_class = config_object or get_config()
    app.config.from_object(config_class)

    # Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Blueprints (API + autenticacion)
    register_blueprints(app)

    # CLI utilitaria: `flask init-db`
    from .cli import register_cli

    register_cli(app)

    # Logs basicos
    logging.basicConfig(level=logging.INFO)

    # Manejadores de error JSON para la API
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Recurso no encontrado"), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify(error="Metodo no permitido"), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify(error="Error interno del servidor"), 500

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Usuario

        return db.session.get(Usuario, int(user_id))

    return app
