
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_conversations():
    response = client.get("/conversations")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_existing_conversation():
    response = client.get("/conversations/conv_001")

    assert response.status_code == 200
    assert response.json()["id"] == "conv_001"


def test_missing_conversation_returns_404():
    response = client.get("/conversations/conv_999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"
