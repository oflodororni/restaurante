from marshmallow import Schema, fields, validate


class PlatoSchema(Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=100))
    descripcion = fields.String(load_default=None)
    precio = fields.Decimal(required=True, places=2, validate=validate.Range(min=0))
    activo = fields.Boolean(load_default=True)
    categoria_id = fields.Integer(required=True)


class PedidoCreateSchema(Schema):
    numero_mesa = fields.Integer(required=True, validate=validate.Range(min=1))
    items = fields.List(
        fields.Nested(
            type(
                "ItemSchema",
                (Schema,),
                {
                    "plato_id": fields.Integer(required=True),
                    "cantidad": fields.Integer(load_default=1, validate=validate.Range(min=1)),
                },
            )
        ),
        required=True,
        validate=validate.Length(min=1),
    )


class EstadoPedidoSchema(Schema):
    estado = fields.String(
        required=True,
        validate=validate.OneOf(
            ["abierto", "enviado", "preparando", "servido", "cerrado", "cancelado"]
        ),
    )
