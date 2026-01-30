from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    query: str
    plan: Optional[str]  # "vector", "graph", or "hybrid"
    vector_results: List[str]
    graph_results: List[str]
    final_answer: Optional[str]
