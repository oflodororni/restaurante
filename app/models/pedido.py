from datetime import datetime, timezone

from app.extensions import db

ESTADOS_PEDIDO = ("abierto", "enviado", "preparando", "servido", "cerrado", "cancelado")


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    numero_mesa = db.Column(db.Integer, nullable=False, index=True)
    estado = db.Column(db.Enum(*ESTADOS_PEDIDO, name="estado_pedido"), default="abierto")
    creada_en = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    cerrada_en = db.Column(db.DateTime)
    camarero_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    camarero = db.relationship("Usuario", back_populates="pedidos")
    lineas = db.relationship(
        "PedidoItem", back_populates="pedido", cascade="all, delete-orphan", lazy="selectin"
    )

    @property
    def total(self) -> float:
        return sum(float(linea.subtotal) for linea in self.lineas)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "numero_mesa": self.numero_mesa,
            "estado": self.estado,
            "creada_en": self.creada_en.isoformat() if self.creada_en else None,
            "camarero_id": self.camarero_id,
            "total": self.total,
            "lineas": [linea.to_dict() for linea in self.lineas],
        }

    def __repr__(self) -> str:
        return f"<Pedido #{self.id} mesa {self.numero_mesa} ({self.estado})>"


class PedidoItem(db.Model):
    __tablename__ = "pedido_items"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    plato_id = db.Column(db.Integer, db.ForeignKey("platos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(8, 2), nullable=False)

    pedido = db.relationship("Pedido", back_populates="lineas")
    plato = db.relationship("Plato", back_populates="lineas_pedido")

    @property
    def subtotal(self) -> float:
        return float(self.precio_unitario) * self.cantidad

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "plato_id": self.plato_id,
            "plato": self.plato.nombre if self.plato else None,
            "cantidad": self.cantidad,
            "precio_unitario": float(self.precio_unitario),
            "subtotal": self.subtotal,
        }
