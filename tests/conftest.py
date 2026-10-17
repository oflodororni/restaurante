import pytest
from sqlalchemy.pool import StaticPool

from app import create_app as _create_app
from app.config import TestingConfig
from app.extensions import db as _db
from app.models import Categoria, Plato, Usuario


@pytest.fixture(scope="session")
def app():
    class Config(TestingConfig):
        # SQLite en memoria compartido entre conexiones del test client
        SQLALCHEMY_DATABASE_URI = "sqlite://"
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
        }

    app = _create_app(Config)
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def db(app):
    """Tablas limpias antes de cada test."""
    _db.session.remove()
    _db.drop_all()
    _db.create_all()
    yield _db
    _db.session.remove()


@pytest.fixture()
def admin(db):
    usuario = Usuario(nombre="Admin", email="admin@test.local", rol="admin")
    usuario.set_password("secreta123")
    camarero = Usuario(nombre="Camarero", email="camarero@test.local", rol="camarero")
    camarero.set_password("secreta123")
    categoria = Categoria(nombre="Principales")
    db.session.add_all([usuario, camarero, categoria])
    db.session.commit()
    db.session.add(Plato(nombre="Solomillo", precio=18.9, categoria=categoria, activo=True))
    db.session.commit()
    return usuario


@pytest.fixture()
def logged_client(client, admin):
    client.post("/auth/login", json={"email": "admin@test.local", "password": "secreta123"})
    return client
