import os
import requests
import json
from src.utils.logger import logger


class LLMClient:
    """
    Client to interact with the local Ray Serve LLM endpoint.
    """

    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("RAY_SERVE_URL", "http://localhost:8000")
        self.endpoint = f"{self.base_url}/generate"

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """
        Sends a prompt to the LLM service and returns the text response.
        """
        # In a real VLLM setup, this might match OpenAI's API or a custom schema.
        # We'll assume a simple JSON schema: {"prompt": "...", "system": "..."}
        payload = {"prompt": prompt}
        if system_prompt:
            payload["system_prompt"] = system_prompt

        try:
            # For development/testing without the service running, we can use a mock if connection fails
            # But for "intensive testing", we should try to hit it or mock the network call in tests.
            response = requests.post(self.endpoint, json=payload, timeout=10)
            response.raise_for_status()
            return response.json().get("text", "")
        except requests.exceptions.ConnectionError:
            # Fallback for dev/test when Docker isn't running
            logger.warning(
                f"Could not connect to {self.endpoint}. Returning mock response."
            )
            return "This is a mock LLM response because the Ray service is unreachable."

    def plan_query(self, query: str) -> str:
        """
        Specialized method to ask the LLM to classify the query.
        """
        system_prompt = (
            "You are a query planner. specific 'vector' for unstructured queries, "
            "'graph' for relationship/entity queries, or 'hybrid' for both. "
            "Reply ONLY with one of those three words."
        )
        response = self.generate(f"Query: {query}", system_prompt=system_prompt)
        cleaned = response.strip().lower()
        if "graph" in cleaned:
            return "graph"
        if "vector" in cleaned:
            return "vector"
        return "hybrid"  # Default safe fallback
