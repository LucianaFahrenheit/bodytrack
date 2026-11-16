import re
from flask import Blueprint, request, jsonify, session
from app.models.usuario_model import criar_usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/cadastro", methods=["POST"])
def cadastro():
    dados = request.get_json() or {}
    nome = (dados.get("nome") or "").strip()
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""
    senha2 = dados.get("senha2") or ""

    # Validações (Passo 5: 400 para dado inválido)
    if len(nome) < 2:
        return jsonify({"campo": "nome", "erro": "Informe seu nome (mínimo 2 letras)."}), 400
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
    return jsonify({"mensagem": "Conta criada com sucesso!", "usuario": usuario}), 201
