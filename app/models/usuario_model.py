import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.conexao import get_db_connection


def criar_usuario(nome, email, senha):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO usuario (nome, email, senha_hash)
            VALUES (%s, %s, %s)
            RETURNING id, nome, email;
            """,
            (nome, email, generate_password_hash(senha)),
        )
        novo = cur.fetchone()
        conn.commit()
        return novo
    except psycopg2.IntegrityError:
        conn.rollback()
        return None  # e-mail já cadastrado
    finally:
        cur.close()
        conn.close()


def buscar_por_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, nome, email, senha_hash FROM usuario WHERE email = %s;",
            (email,),
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def buscar_por_id(usuario_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, nome, email, data_nascimento FROM usuario WHERE id = %s;",
            (usuario_id,),
        )
        u = cur.fetchone()
        if not u:
            return None
        nasc = u["data_nascimento"]
        return {
            "id": u["id"],
            "nome": u["nome"],
            "email": u["email"],
            "nasc": nasc.isoformat() if nasc else "",
        }
    finally:
        cur.close()
        conn.close()


def autenticar(email, senha):
    usuario = buscar_por_email(email)
    if usuario and check_password_hash(usuario["senha_hash"], senha):
        return {"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]}
    return None


def atualizar_usuario(usuario_id, nome, email, nasc, senha=None):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        if senha:
            cur.execute(
                """UPDATE usuario SET nome=%s, email=%s, data_nascimento=%s, senha_hash=%s
                   WHERE id=%s;""",
                (nome, email, nasc, generate_password_hash(senha), usuario_id),
            )
        else:
            cur.execute(
                "UPDATE usuario SET nome=%s, email=%s, data_nascimento=%s WHERE id=%s;",
                (nome, email, nasc, usuario_id),
            )
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        conn.rollback()
        return False  # e-mail já usado por outra usuária
    finally:
        cur.close()
        conn.close()


def excluir_usuario(usuario_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # os registros e medidas são apagados junto (ON DELETE CASCADE)
        cur.execute("DELETE FROM usuario WHERE id = %s;", (usuario_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()
