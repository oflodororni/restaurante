from datetime import datetime, timezone

from flask import abort, jsonify, request
from flask_login import current_user, login_required
from marshmallow import ValidationError

from app.extensions import db
from app.models import Pedido, PedidoItem, Plato

from . import api_bp
from .schemas import EstadoPedidoSchema, PedidoCreateSchema

pedido_schema = PedidoCreateSchema()
estado_schema = EstadoPedidoSchema()


@api_bp.get("/pedidos")
@login_required
def lista_pedidos():
    query = Pedido.query
    estado = request.args.get("estado")
    mesa = request.args.get("numero_mesa", type=int)
    if estado:
        query = query.filter_by(estado=estado)
    if mesa:
        query = query.filter_by(numero_mesa=mesa)
    pedidos = query.order_by(Pedido.creada_en.desc()).all()
    return jsonify([p.to_dict() for p in pedidos])


@api_bp.post("/pedidos")
@login_required
def crear_pedido():
    try:
        data = pedido_schema.load(request.get_json(force=True))
    except ValidationError as err:
        return jsonify(errors=err.messages), 422

    pedido = Pedido(numero_mesa=data["numero_mesa"], camarero_id=current_user.id)
    for item in data["items"]:
        plato = db.session.get(Plato, item["plato_id"])
        if not plato or not plato.activo:
            return jsonify(error=f"Plato {item['plato_id']} no disponible"), 422
        pedido.lineas.append(
            PedidoItem(plato=plato, cantidad=item["cantidad"], precio_unitario=plato.precio)
        )

    db.session.add(pedido)
    db.session.commit()
    return jsonify(pedido.to_dict()), 201


@api_bp.get("/pedidos/<int:pedido_id>")
@login_required
def detalle_pedido(pedido_id):
    pedido = db.session.get(Pedido, pedido_id) or abort(404)
    return jsonify(pedido.to_dict())


@api_bp.patch("/pedidos/<int:pedido_id>/estado")
@login_required
def cambiar_estado(pedido_id):
    pedido = db.session.get(Pedido, pedido_id) or abort(404)
    try:
        data = estado_schema.load(request.get_json(force=True))
    except ValidationError as err:
        return jsonify(errors=err.messages), 422

    pedido.estado = data["estado"]
    if data["estado"] == "cerrado":
        pedido.cerrada_en = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify(pedido.to_dict())
