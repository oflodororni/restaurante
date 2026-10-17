def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"estado": "ok"}


def test_lista_platos_publica(client, db, admin):
    resp = client.get("/api/platos")
    assert resp.status_code == 200
    platos = resp.get_json()
    assert len(platos) == 1
    assert platos[0]["nombre"] == "Solomillo"


def test_crear_plato_requiere_login(client, db):
    resp = client.post("/api/platos", json={"nombre": "X", "precio": 5, "categoria_id": 1})
    assert resp.status_code in (302, 401)


def test_login_y_me(logged_client):
    resp = logged_client.get("/auth/me")
    assert resp.status_code == 200
    assert resp.get_json()["rol"] == "admin"


def test_login_incorrecto(client):
    resp = client.post("/auth/login", json={"email": "no@existe", "password": "mal"})
    assert resp.status_code == 401


def test_admin_puede_crear_plato(logged_client, db, admin):
    from app.models import Categoria

    cat = Categoria.query.filter_by(nombre="Principales").first()
    resp = logged_client.post(
        "/api/platos",
        json={"nombre": "Pisto", "precio": 7.5, "categoria_id": cat.id},
    )
    assert resp.status_code == 201
    assert resp.get_json()["nombre"] == "Pisto"


def test_validacion_error_422(logged_client, db):
    from app.models import Categoria

    cat = Categoria.query.first()
    resp = logged_client.post("/api/platos", json={"precio": -3, "categoria_id": cat.id})
    assert resp.status_code == 422


def test_ciclo_pedido_completo(logged_client, db):
    from app.models import Plato

    plato = Plato.query.filter_by(nombre="Solomillo").first()
    resp = logged_client.post(
        "/api/pedidos",
        json={"numero_mesa": 3, "items": [{"plato_id": plato.id, "cantidad": 2}]},
    )
    assert resp.status_code == 201
    pedido = resp.get_json()
    assert pedido["total"] == 37.8

    resp = logged_client.patch(f"/api/pedidos/{pedido['id']}/estado", json={"estado": "cerrado"})
    assert resp.status_code == 200
    assert resp.get_json()["estado"] == "cerrado"
