import pytest
from unittest.mock import MagicMock, patch
from src.agents.planner import planner_node
from src.agents.state import AgentState
from src.llm.client import LLMClient

# --- Unit Tests for Agents ---

@pytest.fixture
def mock_llm_client():
    with patch("src.agents.planner.LLMClient") as MockClient:
        client_instance = MockClient.return_value
        yield client_instance

def test_planner_agent_vector_strategy(mock_llm_client):
    """Test that the planner correctly identifies a vector strategy."""
    # Setup
    mock_llm_client.plan_query.return_value = "vector"
    state = AgentState(query="find documents about policy", plan=None, vector_results=[], graph_results=[], final_answer=None)
    
    # Execute
    result = planner_node(state)
    
    # Assert
    assert result["plan"] == "vector"
    mock_llm_client.plan_query.assert_called_once_with("find documents about policy")

def test_planner_agent_graph_strategy(mock_llm_client):
    """Test that the planner correctly identifies a graph strategy."""
    # Setup
    mock_llm_client.plan_query.return_value = "graph"
    state = AgentState(query="how is entity A related to B?", plan=None, vector_results=[], graph_results=[], final_answer=None)
    
    # Execute
    result = planner_node(state)
    
    # Assert
    assert result["plan"] == "graph"

# --- Test LLM Client ---

def test_llm_client_fallback():
    """Test that the LLM client falls back to mock response when service is down."""
    client = LLMClient(base_url="http://bad-url:9999")
    response = client.generate("test")
    assert "mock LLM response" in response
