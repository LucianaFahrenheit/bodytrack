import re
from flask import Blueprint, request, jsonify, session
from app.models.usuario_model import criar_usuario, autenticar, buscar_por_id

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/cadastro", methods=["POST"])
def cadastro():
    dados = request.get_json() or {}
    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""
    senha2 = dados.get("senha2") or ""

    if len(nome) < 2:
        return jsonify({"campo": "nome", "erro": "Informe seu nome."}), 400
    if not re.match(r"^\S+@\S+\.\S+$", email):
        return jsonify({"campo": "email", "erro": "Informe um e-mail válido."}), 400
    if len(senha) < 6:
        return jsonify({"campo": "senha", "erro": "A senha precisa ter ao menos 6 caracteres."}), 400
    if senha != senha2:
        return jsonify({"campo": "senha2", "erro": "As senhas não coincidem."}), 400

    usuario = criar_usuario(nome, email, senha)
    if not usuario:
        return jsonify({"campo": "email", "erro": "Este e-mail já está cadastrado."}), 400

    session["usuario_id"] = usuario["id"]
    return jsonify({"mensagem": "Conta criada com sucesso.", "usuario": usuario}), 201


@auth_bp.route("/api/login", methods=["POST"])
def login():
    dados = request.get_json() or {}
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    if not email or not senha:
        return jsonify({"campo": "senha", "erro": "Informe e-mail e senha."}), 400

    usuario = autenticar(email, senha)
    if not usuario:
        return jsonify({"campo": "senha", "erro": "E-mail ou senha incorretos."}), 401

    session["usuario_id"] = usuario["id"]
    primeiro_nome = usuario["nome"].split(" ")[0]
    return jsonify({"mensagem": f"Bem-vinda de volta, {primeiro_nome}.", "usuario": usuario})


@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensagem": "Você saiu da conta."})


@auth_bp.route("/api/me")
def quem_sou_eu():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return jsonify({"erro": "Não autenticada."}), 401
    usuario = buscar_por_id(usuario_id)
    if not usuario:
        session.clear()
        return jsonify({"erro": "Não autenticada."}), 401
    return jsonify({"usuario": usuario})
