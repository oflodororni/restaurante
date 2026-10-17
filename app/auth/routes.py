from flask import jsonify, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.models import Usuario

from . import auth_bp


@auth_bp.post("/login")
def login():
    """Login por formulario o JSON: {email, password}."""
    data = request.get_json(silent=True) or request.form
    usuario = Usuario.query.filter_by(email=data.get("email", "")).first()

    if not usuario or not usuario.check_password(data.get("password", "")):
        return jsonify(error="Credenciales invalidas"), 401
    if not usuario.activo:
        return jsonify(error="Usuario desactivado"), 403

    login_user(usuario)
    if request.is_json:
        return jsonify(mensaje="Sesion iniciada", usuario=usuario.to_dict())
    return redirect(url_for("api.lista_platos"))


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    return jsonify(mensaje="Sesion cerrada")


@auth_bp.get("/me")
@login_required
def me():
    return jsonify(current_user.to_dict())
