import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.main import app

client = TestClient(app)


@pytest.fixture
def mock_graph_app():
    with patch("src.api.main.graph_app") as mock_app:
        yield mock_app


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_query_endpoint(mock_graph_app):
    """Test the /query endpoint calls the graph and returns results."""
    # Setup mock return from graph
    mock_graph_app.invoke.return_value = {
        "final_answer": "Test Answer",
        "plan": "hybrid",
    }

    payload = {"query": "test query"}
    headers = {"X-API-Key": "secret-enterprise-key"}

    # We must mock the environment variable or ensure the default matches what we send
    with patch.dict(
        os.environ, {"GRAPH_RAG_API_KEY": "secret-enterprise-key", "ENV": "production"}
    ):
        response = client.post("/query", json=payload, headers=headers)

    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["answer"] == "Test Answer"
    assert json_resp["execution_plan"] == "hybrid"

    # Verify invoke was called with correct initial state
    mock_graph_app.invoke.assert_called_once()
    call_args = mock_graph_app.invoke.call_args[0][0]
    assert call_args["query"] == "test query"
