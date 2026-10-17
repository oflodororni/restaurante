from flask import Blueprint

api_bp = Blueprint("api", __name__)

from . import pedidos, platos  # noqa: E402,F401
