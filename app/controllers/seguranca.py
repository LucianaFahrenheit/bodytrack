from functools import wraps
from flask import session, jsonify


def login_obrigatorio(f):
    """Bloqueia a rota se a usuária não estiver logada (erro 401)."""
    @wraps(f)
    def interna(*args, **kwargs):
        if not session.get("usuario_id"):
            return jsonify({"erro": "Faça login para continuar."}), 401
        return f(*args, **kwargs)
    return interna
