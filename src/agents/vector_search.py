from src.agents.state import AgentState
from qdrant_client import QdrantClient
import os
from src.utils.logger import logger


def vector_search_node(state: AgentState) -> AgentState:
    """
    Performs semantic search using Qdrant.
    """
    query = state["query"]
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")

    logger.info(f"Vector Search: Searching for '{query}'")

    try:
        # client = QdrantClient(url=qdrant_url)
        # results = client.search(collection_name="enterprise_docs", query_vector=embed(query), limit=5)
        # mock results:
        results = [f"Vector Result 1 for {query}", f"Vector Result 2 for {query}"]
    except Exception as e:
        logger.error(f"Vector search failed: {e}")
        results = ["Error retrieving vector results"]

    return {"vector_results": results}
