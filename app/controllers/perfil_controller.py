import re
from datetime import date
from flask import Blueprint, request, jsonify, session
from app.controllers.seguranca import login_obrigatorio
from app.models.usuario_model import buscar_por_id, atualizar_usuario, excluir_usuario

perfil_bp = Blueprint("perfil", __name__)


@perfil_bp.route("/api/perfil", methods=["PUT"])
@login_obrigatorio
def editar_perfil():
    dados = request.get_json() or {}
    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()
    nasc_txt = (dados.get("nasc") or "").strip()
    senha = dados.get("senha") or ""
    erros = {}

    if len(nome) < 2:
        erros["nome"] = "Informe seu nome."
    if not re.match(r"^\S+@\S+\.\S+$", email):
        erros["email"] = "Informe um e-mail válido."
    nasc = None
    if nasc_txt:
        try:
            nasc = date.fromisoformat(nasc_txt)
        except ValueError:
            erros["nasc"] = "Data inválida."
        else:
            if nasc > date.today():
                erros["nasc"] = "A data de nascimento não pode ser futura."
    if senha and len(senha) < 6:
        erros["senha"] = "A senha precisa ter ao menos 6 caracteres."
    if erros:
        return jsonify({"erros": erros}), 400

    usuario_id = session["usuario_id"]
    if not atualizar_usuario(usuario_id, nome, email, nasc, senha or None):
        return jsonify({"erros": {"email": "Este e-mail já está em uso."}}), 400
    return jsonify({"mensagem": "Perfil atualizado.", "usuario": buscar_por_id(usuario_id)})


@perfil_bp.route("/api/perfil", methods=["DELETE"])
@login_obrigatorio
def excluir_conta():
    excluir_usuario(session["usuario_id"])
    session.clear()
    return jsonify({"mensagem": "Conta excluída."})
