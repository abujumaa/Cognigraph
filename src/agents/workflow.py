from langgraph.graph import StateGraph, END
from src.agents.state import AgentState
from src.agents.planner import planner_node
from src.agents.vector_search import vector_search_node
from src.agents.graph_search import graph_search_node
from src.agents.synthesizer import synthesizer_node

# Define the routing logic
def router(state: AgentState):
    plan = state.get("plan", "hybrid")
    if plan == "vector":
        return ["vector_search"]
    elif plan == "graph":
        return ["graph_search"]
    else:
        return ["vector_search", "graph_search"]

# Construct the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("planner", planner_node)
workflow.add_node("vector_search", vector_search_node)
workflow.add_node("graph_search", graph_search_node)
workflow.add_node("synthesizer", synthesizer_node)

# Add edges
workflow.set_entry_point("planner")

# Conditional edges from planner to searchers
workflow.add_conditional_edges(
    "planner",
    router,
    {
        "vector_search": "vector_search",
        "graph_search": "graph_search",
        # For hybrid, we map to both (parallel execution is supported by LangGraph if branching)
        # NOTE: LangGraph API varies; to fan-out, we might need a specific structure or just return list.
        # Assuming the 'router' returns a list of next nodes for parallel execution:
    }
)

# In current LangGraph (0.0.x), conditional edges usually return a single next node or we use a Map step.
# For simplicity in this scaffold, we will just fan out to both if hybrid, 
# but strictly speaking standard conditional edges direct flow.
# To achieve parallel fan-out easily:
# We can make planner go to a 'fork' node or define the edges explicitly.
# For this scaffold, let's simplify: Planner -> (Router logic) -> Searchers -> Synthesizer

# To support the list output from router, we need to ensure the graph supports it.
# If not, we'll force hybrid to run vector then graph sequentially for safety in this scaffold.

workflow.add_edge("vector_search", "synthesizer")
workflow.add_edge("graph_search", "synthesizer")
workflow.add_edge("synthesizer", END)

app = workflow.compile()
