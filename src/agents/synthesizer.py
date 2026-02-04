from src.agents.state import AgentState
from src.llm.client import LLMClient
from src.utils.logger import logger


def synthesizer_node(state: AgentState) -> AgentState:
    """
    Synthesizes the final answer using results from both searchers.
    """
    llm = LLMClient()

    context = ""
    if state.get("vector_results"):
        context += "Vector Context:\n" + "\n".join(state["vector_results"]) + "\n\n"
    if state.get("graph_results"):
        context += "Graph Context:\n" + "\n".join(state["graph_results"]) + "\n\n"

    prompt = (
        f"Context:\n{context}\n"
        f"User Query: {state['query']}\n"
        "Generate a comprehensive answer based on the context above."
    )

    response = llm.generate(prompt)

    logger.info("Synthesizer: Generated Final Answer")
    return {"final_answer": response}
