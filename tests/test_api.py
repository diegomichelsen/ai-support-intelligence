"""
Testes da API do AI Support Intelligence.

O banco de dados é substituído por um banco falso (fake) em memória.
Assim os testes rodam em qualquer máquina e no GitHub Actions,
sem precisar de PostgreSQL nem de credenciais.
"""

import pytest
from fastapi.testclient import TestClient

from src.api import main
from src.api.main import app

client = TestClient(app)

# Dados fictícios que o banco falso vai "devolver"
CONVERSATIONS = [
    {"id": "conv_001", "brand_id": "brand_alpha", "channel": "chat"},
    {"id": "conv_002", "brand_id": "brand_beta", "channel": "email"},
    {"id": "conv_003", "brand_id": "brand_alpha", "channel": "whatsapp"},
]


class FakeCursor:
    """Imita o cursor do psycopg: recebe o SQL e responde com dados da lista acima."""

    def __init__(self):
        self._result = []

    def execute(self, sql, params=None):
        sql = " ".join(sql.split())  # remove quebras de linha para facilitar a comparação
        if "COUNT(*)" in sql:
            self._result = [(len(CONVERSATIONS),)]
        elif "WHERE id" in sql:
            self._result = [(c,) for c in CONVERSATIONS if c["id"] == params[0]]
        else:
            limit, offset = params
            self._result = [(c,) for c in CONVERSATIONS[offset:offset + limit]]

    def fetchone(self):
        return self._result[0] if self._result else None

    def fetchall(self):
        return self._result

    # Permite usar "with conn.cursor() as cursor:" igual ao código real
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FakeConnection:
    def cursor(self):
        return FakeCursor()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


@pytest.fixture
def fake_db(monkeypatch):
    """Troca a conexão real pela falsa apenas durante o teste que pedir esta fixture."""
    monkeypatch.setattr(main, "get_connection", lambda: FakeConnection())


# ---------- /health ----------

def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------- /conversations: validações (não chegam a tocar no banco) ----------

@pytest.mark.parametrize("query", ["limit=0", "limit=101", "offset=-1"])
def test_conversations_rejects_invalid_pagination(query):
    response = client.get(f"/conversations?{query}")

    assert response.status_code == 400


# ---------- /conversations: paginação ----------

def test_conversations_returns_first_page_with_metadata(fake_db):
    response = client.get("/conversations?limit=2&offset=0")
    body = response.json()

    assert response.status_code == 200
    assert body["total"] == 3
    assert body["returned"] == 2
    assert body["has_more"] is True
    assert [c["id"] for c in body["data"]] == ["conv_001", "conv_002"]


def test_conversations_last_page_has_no_more(fake_db):
    body = client.get("/conversations?limit=2&offset=2").json()

    assert body["returned"] == 1
    assert body["has_more"] is False


# ---------- /conversations/{id} ----------

def test_get_conversation_by_id(fake_db):
    response = client.get("/conversations/conv_002")

    assert response.status_code == 200
    assert response.json()["brand_id"] == "brand_beta"


def test_get_conversation_not_found_returns_404(fake_db):
    response = client.get("/conversations/nao_existe")

    assert response.status_code == 404
