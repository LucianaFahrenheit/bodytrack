# Ponto de entrada para o servidor de produção (gunicorn).
# Carrega o app.py da raiz, porque "app" também é o nome da pasta do projeto.
import importlib.util
import sys
from pathlib import Path

raiz = Path(__file__).resolve().parent
sys.path.insert(0, str(raiz))

spec = importlib.util.spec_from_file_location("bodytrack_main", raiz / "app.py")
modulo = importlib.util.module_from_spec(spec)
sys.modules["bodytrack_main"] = modulo
spec.loader.exec_module(modulo)

application = modulo.app
