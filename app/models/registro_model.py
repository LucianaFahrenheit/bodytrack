from decimal import Decimal
import psycopg2.errors
from app.models.conexao import get_db_connection

# nome no banco (tabela tipo_medida) -> chave usada no front-end
CHAVES = {
    "Cintura": "cintura",
    "Quadril": "quadril",
    "Coxas": "coxas",
    "Panturrilhas": "panturrilhas",
    "Braços": "bracos",
    "Peitoral": "peitoral",
}


def _num(v):
    return float(v) if isinstance(v, Decimal) else v


def _tipos(cur):
    cur.execute("SELECT id, nome FROM tipo_medida;")
    return {CHAVES[r["nome"]]: r["id"] for r in cur.fetchall() if r["nome"] in CHAVES}


def _gravar_medidas(cur, registro_id, dados):
    for chave, tipo_id in _tipos(cur).items():
        valor = dados.get(chave)
        if valor is not None:
            cur.execute(
                """INSERT INTO medida (registro_id, tipo_medida_id, valor_cm)
                   VALUES (%s, %s, %s);""",
                (registro_id, tipo_id, valor),
            )


def listar(usuario_id):
    """Todos os registros da usuária (sempre filtrando por usuario_id)."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT id, data_registro, peso_kg, altura_cm, observacoes
               FROM registro WHERE usuario_id = %s ORDER BY data_registro;""",
            (usuario_id,),
        )
        saida = {}
        for r in cur.fetchall():
            item = {
                "id": r["id"],
                "data": r["data_registro"].isoformat(),
                "peso": _num(r["peso_kg"]),
                "altura": _num(r["altura_cm"]),
                "obs": r["observacoes"] or "",
            }
            item.update({chave: None for chave in CHAVES.values()})
            saida[r["id"]] = item
        if saida:
            cur.execute(
                """SELECT m.registro_id, t.nome, m.valor_cm
                   FROM medida m
                   JOIN tipo_medida t ON t.id = m.tipo_medida_id
                   JOIN registro r ON r.id = m.registro_id
                   WHERE r.usuario_id = %s;""",
                (usuario_id,),
            )
            for m in cur.fetchall():
                chave = CHAVES.get(m["nome"])
                if chave and m["registro_id"] in saida:
                    saida[m["registro_id"]][chave] = _num(m["valor_cm"])
        return list(saida.values())
    finally:
        cur.close()
        conn.close()


def criar(usuario_id, d):
    """Cria o registro. Devolve o id, ou None se a data já existe."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO registro (usuario_id, data_registro, peso_kg, altura_cm, observacoes)
               VALUES (%s, %s, %s, %s, %s) RETURNING id;""",
            (usuario_id, d["data"], d["peso"], d["altura"], d["obs"] or None),
        )
        novo_id = cur.fetchone()["id"]
        _gravar_medidas(cur, novo_id, d)
        conn.commit()
        return novo_id
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()


def atualizar(usuario_id, registro_id, d):
    """Devolve 'ok', 'nao_encontrado' ou 'duplicado'."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """UPDATE registro
               SET data_registro=%s, peso_kg=%s, altura_cm=%s, observacoes=%s
               WHERE id=%s AND usuario_id=%s;""",
            (d["data"], d["peso"], d["altura"], d["obs"] or None, registro_id, usuario_id),
        )
        if cur.rowcount == 0:
            conn.rollback()
            return "nao_encontrado"
        cur.execute("DELETE FROM medida WHERE registro_id = %s;", (registro_id,))
        _gravar_medidas(cur, registro_id, d)
        conn.commit()
        return "ok"
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return "duplicado"
    finally:
        cur.close()
        conn.close()


def excluir(usuario_id, registro_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM registro WHERE id = %s AND usuario_id = %s;",
            (registro_id, usuario_id),
        )
        conn.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        conn.close()
