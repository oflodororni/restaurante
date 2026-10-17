from flask import Flask
from .config import DevelopmentConfig
from .extensions import db, migrate


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Aquí registraremos los blueprints en pasos siguientes
    # register_blueprints(app)

    return app