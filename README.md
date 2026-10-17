# Restaurant DB

Aplicacion Flask para gestion de restaurante: menu, pedidos y usuarios con roles.

## Stack

- Flask 3 + factory pattern
- Flask-SQLAlchemy / Flask-Migrate (MySQL en dev/prod, SQLite en memoria en tests)
- Flask-Login (sesiones) + roles: `admin`, `camarero`, `cocina`
- marshmallow (validacion de payloads JSON)
- pytest, ruff, black

## Puesta en marcha

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # y edita SECRET_KEY / DATABASE_URL

# Base de datos (opcional: docker compose up -d mysql)
make init-db seed           # crea tablas + datos de ejemplo
make run                    # http://localhost:5000
```

Produccion: `FLASK_ENV=prod` (falla al arrancar si el SECRET_KEY sigue siendo el de ejemplo).

## API

| Metodo | Ruta | Auth | Descripcion |
|---|---|---|---|
| GET | `/api/health` | - | Estado del servicio |
| GET | `/api/categorias` | - | Listado de categorias |
| GET | `/api/platos` | - | Menu (`?categoria_id=`, `?solo_activos=0`) |
| GET | `/api/platos/<id>` | - | Detalle de plato |
| POST/PATCH | `/api/platos[/<id>]` | admin | Alta/edicion de plato |
| DELETE | `/api/platos/<id>` | admin | Borrado logico (desactivar) |
| POST | `/auth/login` | - | `{email, password}` -> sesion |
| POST | `/auth/logout` | login | Cerrar sesion |
| GET | `/auth/me` | login | Usuario actual |
| GET/POST | `/api/pedidos` | login | Listar / crear pedido |
| GET | `/api/pedidos/<id>` | login | Detalle |
| PATCH | `/api/pedidos/<id>/estado` | login | Transicion de estado |

Estados de pedido: abierto → enviado → preparando → servido → cerrado (o cancelado).

## Migraciones

```bash
flask db init      # una sola vez
flask db migrate -m "mensaje"
flask db upgrade
```

## Tests y calidad

```bash
make test    # pytest (SQLite en memoria, aislado con rollback)
make lint    # ruff + black --check
make format  # black + ruff --fix
```

## Estructura

```
app/
  __init__.py      # factory create_app + errores JSON
  config.py        # dev/prod/test + get_config() por FLASK_ENV
  extensions.py    # db, migrate, login_manager, register_blueprints
  cli.py           # flask init-db / flask seed
  models/          # usuario, menu (Categoria/Plato), pedido (Pedido/PedidoItem)
  auth/            # blueprint de sesiones
  api/             # blueprints REST + schemas marshmallow
tests/             # pytest con fixtures de app/client/db
```
