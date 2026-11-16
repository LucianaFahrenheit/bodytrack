import os, psycopg2
from dotenv import load_dotenv

load_dotenv()
print("Senha lida do .env:", "SIM" if os.getenv("DB_PASSWORD") else "NÃO (vazia)")
try:
    psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "bodytrack"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )
    print("Conectou!")
except UnicodeDecodeError as e:
    print("Erro real:", e.object.decode("latin-1"))
except Exception as e:
    print("Erro:", e) 