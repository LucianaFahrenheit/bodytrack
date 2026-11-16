import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.conexao import get_db_connection


def criar_usuario(nome, email, senha):
    conn = get_db_connection()
    cur = conn.cursor()
    senha_hash = generate_password_hash(senha)
    try:
        cur.execute(
            """
            INSERT INTO usuario (nome, email, senha_hash)
            VALUES (%s, %s, %s)
            RETURNING id, nome, email;
            """,
            (nome, email, senha_hash),
        )
        novo_usuario = cur.fetchone()
        conn.commit()
        return novo_usuario
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
            "SELECT id, nome, email FROM usuario WHERE id = %s;",
            (usuario_id,),
        )
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()


def autenticar(email, senha):
    usuario = buscar_por_email(email)
    if usuario and check_password_hash(usuario["senha_hash"], senha):
        return {"id": usuario["id"], "nome": usuario["nome"], "email": usuario["email"]}
    return None
