from datetime import date
from flask import Blueprint, request, jsonify, session
from app.controllers.seguranca import login_obrigatorio
from app.models import registro_model

reg_bp = Blueprint("registros", __name__)

MEDIDAS = ["cintura", "quadril", "coxas", "panturrilhas", "bracos", "peitoral"]
REGRAS = {"peso": (20, 400), "altura": (80, 250)}
REGRAS.update({m: (10, 250) for m in MEDIDAS})


def validar(dados):
    """Valida os dados de um registro. Devolve (dados_limpos, erros)."""
    erros = {}
    limpo = {}

    data_txt = (dados.get("data") or "").strip()
    try:
        d = date.fromisoformat(data_txt)
    except ValueError:
        erros["data"] = "Informe uma data válida."
        limpo["data"] = None
    else:
        if d > date.today():
            erros["data"] = "Escolha uma data que não seja futura."
        limpo["data"] = d

    for campo, (minimo, maximo) in REGRAS.items():
        bruto = dados.get(campo)
        if bruto is None or bruto == "":
            limpo[campo] = None
            continue
        try:
            n = float(str(bruto).replace(",", "."))
        except ValueError:
            erros[campo] = "Informe um número válido."
            continue
        if n < minimo or n > maximo:
            erros[campo] = f"Informe um valor entre {minimo} e {maximo}."
            continue
        limpo[campo] = n

    if not erros and limpo["peso"] is None and all(limpo[m] is None for m in MEDIDAS):
        erros["peso"] = "Preencha o peso ou ao menos uma medida."

    limpo["obs"] = (dados.get("obs") or "").strip()[:300]
    return limpo, erros


@reg_bp.route("/api/registros", methods=["GET"])
@login_obrigatorio
def listar_registros():
    return jsonify({"registros": registro_model.listar(session["usuario_id"])})


@reg_bp.route("/api/registros", methods=["POST"])
@login_obrigatorio
def criar_registro():
    limpo, erros = validar(request.get_json() or {})
    if erros:
        return jsonify({"erros": erros}), 400
    novo_id = registro_model.criar(session["usuario_id"], limpo)
    if novo_id is None:
        return jsonify({"erros": {"data": "Já existe um registro nesta data."}}), 409
    return jsonify({"mensagem": "Registro salvo.", "id": novo_id}), 201


@reg_bp.route("/api/registros/<int:registro_id>", methods=["PUT"])
@login_obrigatorio
def editar_registro(registro_id):
    limpo, erros = validar(request.get_json() or {})
    if erros:
        return jsonify({"erros": erros}), 400
    resultado = registro_model.atualizar(session["usuario_id"], registro_id, limpo)
    if resultado == "nao_encontrado":
        return jsonify({"erro": "Registro não encontrado."}), 404
    if resultado == "duplicado":
        return jsonify({"erros": {"data": "Já existe um registro nesta data."}}), 409
    return jsonify({"mensagem": "Registro atualizado."})


@reg_bp.route("/api/registros/<int:registro_id>", methods=["DELETE"])
@login_obrigatorio
def excluir_registro(registro_id):
    if not registro_model.excluir(session["usuario_id"], registro_id):
        return jsonify({"erro": "Registro não encontrado."}), 404
    return jsonify({"mensagem": "Registro excluído."})
