import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    try:
        url = os.getenv("DATABASE_URL")  # usado na hospedagem (Render)
        if url:
            return psycopg2.connect(url, cursor_factory=RealDictCursor)
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            dbname=os.getenv("DB_NAME", "bodytrack"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            cursor_factory=RealDictCursor,
        )
    except UnicodeDecodeError as e:
        # a mensagem de erro do Windows vem acentuada e o Python não consegue ler
        mensagem = e.object.decode("latin-1")
        raise RuntimeError("Falha ao conectar no PostgreSQL: " + mensagem) from None
