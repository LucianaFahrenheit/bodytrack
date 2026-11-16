import psycopg2
from werkzeug.security import generate_password_hash
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
            (nome, email, senha_hash)
        )
        novo_usuario = cur.fetchone()
        conn.commit()
        return novo_usuario
    except psycopg2.IntegrityError:
        conn.rollback()
        return None  # E-mail já cadastrado (viola UQ email)
    finally:
        cur.close()
        conn.close()
        