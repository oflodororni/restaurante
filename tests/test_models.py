from app.models import Categoria, Pedido, PedidoItem, Plato, Usuario


def test_password_hashing(db):
    u = Usuario(nombre="Ana", email="ana@test.local", rol="cocina")
    u.set_password("clave123")
    assert u.password_hash != "clave123"
    assert u.check_password("clave123")
    assert not u.check_password("otra")


def test_pedido_total(db):
    cat = Categoria(nombre="Postres")
    plato = Plato(nombre="Tarta", precio=6.0, categoria=cat, activo=True)
    pedido = Pedido(numero_mesa=1)
    pedido.lineas.append(PedidoItem(plato=plato, cantidad=3, precio_unitario=plato.precio))
    db.session.add_all([cat, plato, pedido])
    db.session.commit()
    assert pedido.total == 18.0
