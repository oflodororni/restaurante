import click
from flask.cli import with_appcontext

from .extensions import db


@click.command(name="init-db")
@with_appcontext
def init_db_command():
    """Crea las tablas (uso en desarrollo; en prod usa flask db migrate)."""
    from app import models  # noqa: F401 - registra los modelos

    db.create_all()
    click.echo("Base de datos inicializada.")


@click.command(name="seed")
@with_appcontext
def seed_command():
    """Inserta datos de ejemplo (categorias, platos, mesas, usuario admin)."""
    from app.models import Categoria, Plato, Usuario

    if not Usuario.query.filter_by(email="admin@restaurant.local").first():
        admin = Usuario(nombre="Admin", email="admin@restaurant.local", rol="admin")
        admin.set_password("admin123")
        db.session.add(admin)

    for nombre in ["Entrantes", "Principales", "Postres", "Bebidas"]:
        if not Categoria.query.filter_by(nombre=nombre).first():
            db.session.add(Categoria(nombre=nombre))

    db.session.commit()

    if not Plato.query.first():
        cats = {c.nombre: c for c in Categoria.query.all()}
        ejemplos = [
            ("Bravas", "Entrantes", 6.5),
            ("Croquetas de jamon", "Entrantes", 8.0),
            ("Solomillo al momento", "Principales", 18.9),
            ("Arroz caldoso de marisco", "Principales", 16.5),
            ("Tarta de queso", "Postres", 6.0),
            ("Cafe solo", "Bebidas", 1.6),
            ("Agua mineral", "Bebidas", 2.0),
        ]
        for nombre, cat, precio in ejemplos:
            db.session.add(Plato(nombre=nombre, categoria=cats[cat], precio=precio, activo=True))
        db.session.commit()

    click.echo("Datos de ejemplo insertados.")


def register_cli(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_command)
