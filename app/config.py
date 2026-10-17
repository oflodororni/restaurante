import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:root@localhost:3306/restaurant_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    def __init__(self):
        super().__init__()
        # En producción es obligatorio cambiar la clave por defecto.
        if self.SECRET_KEY in {"change-me-in-production", "dev-secret-key"}:
            raise RuntimeError("SECRET_KEY inseguro en produccion: define una clave fuerte en .env")


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


config_map = {
    "dev": DevelopmentConfig,
    "development": DevelopmentConfig,
    "prod": ProductionConfig,
    "production": ProductionConfig,
    "test": TestingConfig,
    "testing": TestingConfig,
}


def get_config(env=None):
    """Devuelve la clase de config segun FLASK_ENV (dev|prod|test)."""
    env = env or os.getenv("FLASK_ENV", "dev")
    try:
        return config_map[env.lower()]
    except KeyError:
        raise ValueError(f"FLASK_ENV desconocido: {env!r}. Usa dev|prod|test.") from None
