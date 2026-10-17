from flask import abort, jsonify, request
from flask_login import current_user, login_required
from marshmallow import ValidationError

from app.extensions import db
from app.models import Categoria, Plato

from . import api_bp
from .schemas import PlatoSchema

plato_schema = PlatoSchema()


@api_bp.get("/health")
def health():
    return jsonify(estado="ok")


@api_bp.get("/categorias")
def lista_categorias():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return jsonify([c.to_dict() for c in categorias])


@api_bp.get("/platos")
def lista_platos():
    query = Plato.query
    categoria_id = request.args.get("categoria_id", type=int)
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    if request.args.get("solo_activos", "1") == "1":
        query = query.filter_by(activo=True)
    platos = query.order_by(Plato.nombre).all()
    return jsonify([p.to_dict() for p in platos])


@api_bp.get("/platos/<int:plato_id>")
def detalle_plato(plato_id):
    plato = db.session.get(Plato, plato_id) or abort(404)
    return jsonify(plato.to_dict())


@api_bp.post("/platos")
@login_required
def crear_plato():
    if not current_user.es_admin():
        return jsonify(error="Se requiere rol admin"), 403
    try:
        data = plato_schema.load(request.get_json(force=True))
    except ValidationError as err:
        return jsonify(errors=err.messages), 422

    plato = Plato(**data)
    db.session.add(plato)
    db.session.commit()
    return jsonify(plato.to_dict()), 201


@api_bp.patch("/platos/<int:plato_id>")
@login_required
def actualizar_plato(plato_id):
    if not current_user.es_admin():
        return jsonify(error="Se requiere rol admin"), 403
    plato = db.session.get(Plato, plato_id) or abort(404)
    try:
        data = plato_schema.partial().load(request.get_json(force=True))
    except ValidationError as err:
        return jsonify(errors=err.messages), 422

    for campo, valor in data.items():
        setattr(plato, campo, valor)
    db.session.commit()
    return jsonify(plato.to_dict())


@api_bp.delete("/platos/<int:plato_id>")
@login_required
def desactivar_plato(plato_id):
    """Borrado logico: desactiva el plato sin perder historial de pedidos."""
    if not current_user.es_admin():
        return jsonify(error="Se requiere rol admin"), 403
    plato = db.session.get(Plato, plato_id) or abort(404)
    plato.activo = False
    db.session.commit()
    return jsonify(mensaje="Plato desactivado", plato=plato.to_dict())
