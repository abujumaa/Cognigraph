from src.agents.state import AgentState
from src.llm.client import LLMClient
from src.utils.logger import logger

def planner_node(state: AgentState) -> AgentState:
    """
    Decides the execution strategy based on the user query.
    """
    query = state["query"]
    llm = LLMClient()
    
    # In a real scenario, the LLM analyzes the complexity
    plan = llm.plan_query(query)
    
    logger.info(f"Planner: Decided on {plan} strategy for query: '{query}'")
    return {"plan": plan}