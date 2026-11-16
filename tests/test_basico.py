import sys
import importlib.util
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

# carrega o app.py da raiz (o nome "app" também é a pasta do projeto)
spec = importlib.util.spec_from_file_location("bodytrack_main", RAIZ / "app.py")
modulo = importlib.util.module_from_spec(spec)
sys.modules["bodytrack_main"] = modulo
spec.loader.exec_module(modulo)

from app.controllers.registro_controller import validar  # noqa: E402


@pytest.fixture
def client():
    modulo.app.config["TESTING"] = True
    with modulo.app.test_client() as c:
        yield c


# ---------- validação de registros ----------
def test_registro_valido():
    limpo, erros = validar({"data": "2020-01-10", "peso": 68.5})
    assert erros == {}
    assert limpo["peso"] == 68.5


def test_peso_acima_do_limite():
    _, erros = validar({"data": "2020-01-10", "peso": 500})
    assert "peso" in erros


def test_peso_abaixo_do_limite():
    _, erros = validar({"data": "2020-01-10", "peso": 10})
    assert "peso" in erros


def test_data_futura():
    _, erros = validar({"data": "2999-01-01", "peso": 70})
    assert "data" in erros


def test_registro_vazio():
    _, erros = validar({"data": "2020-01-10"})
    assert "peso" in erros


def test_medida_fora_do_limite():
    _, erros = validar({"data": "2020-01-10", "cintura": 5})
    assert "cintura" in erros


def test_aceita_virgula_decimal():
    limpo, erros = validar({"data": "2020-01-10", "peso": "68,5"})
    assert erros == {} and limpo["peso"] == 68.5


# ---------- acesso sem login (401) ----------
def test_registros_exigem_login(client):
    assert client.get("/api/registros").status_code == 401


def test_criar_registro_exige_login(client):
    assert client.post("/api/registros", json={}).status_code == 401


def test_perfil_exige_login(client):
    assert client.put("/api/perfil", json={}).status_code == 401


def test_me_sem_login(client):
    assert client.get("/api/me").status_code == 401


# ---------- validação do cadastro (400, sem tocar no banco) ----------
def test_cadastro_senha_curta(client):
    r = client.post("/api/cadastro", json={"nome": "Ana", "email": "a@a.com", "senha": "123", "senha2": "123"})
    assert r.status_code == 400


def test_cadastro_senhas_diferentes(client):
    r = client.post("/api/cadastro", json={"nome": "Ana", "email": "a@a.com", "senha": "123456", "senha2": "654321"})
    assert r.status_code == 400


def test_cadastro_email_invalido(client):
    r = client.post("/api/cadastro", json={"nome": "Ana", "email": "invalido", "senha": "123456", "senha2": "123456"})
    assert r.status_code == 400


def test_login_sem_dados(client):
    assert client.post("/api/login", json={}).status_code == 400
