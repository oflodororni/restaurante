from app.extensions import db


class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), unique=True, nullable=False)
    platos = db.relationship("Plato", back_populates="categoria", lazy="dynamic")

    def to_dict(self) -> dict:
        return {"id": self.id, "nombre": self.nombre}

    def __repr__(self) -> str:
        return f"<Categoria {self.nombre}>"


class Plato(db.Model):
    __tablename__ = "platos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(8, 2), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)

    categoria = db.relationship("Categoria", back_populates="platos")
    lineas_pedido = db.relationship("PedidoItem", back_populates="plato")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": float(self.precio),
            "activo": self.activo,
            "categoria_id": self.categoria_id,
        }

    def __repr__(self) -> str:
        return f"<Plato {self.nombre}>"
