import time
import random
from src.utils.logger import logger

def simulate_enterprise_activity():
    logger.info("Starting Enterprise GraphRAG System Simulation...")
    
    users = ["alice.doe", "bob.smith", "charlie.lee", "admin"]
    queries = [
        "Quarterly financial report 2024",
        "HR policies for remote work",
        "Engineering architectural diagrams",
        "Compliance audit for vendor X"
    ]
    
    for _ in range(15):
        user = random.choice(users)
        query = random.choice(queries)
        
        logger.info(f"User '{user}' initiated query: '{query}'")
        
        # Simulate planner
        strategy = random.choice(["vector", "graph", "hybrid"])
        logger.debug(f"Planner Agent: Analyzing complexity... Strategy selected: {strategy}")
        
        if random.random() < 0.1:
            logger.warning(f"Planner: Low confidence in intent classification for '{query}'")
        
        # Simulate processing
        time.sleep(0.1)
        logger.debug("Connecting to Qdrant...")
        logger.debug("Connecting to Neo4j...")
        
        if random.random() < 0.05:
            logger.error("ConnectionTimeout: Neo4j did not respond within 3000ms.")
            continue
            
        logger.info(f"Retrieved 5 vector chunks and 3 graph subgraphs.")
        logger.debug("Synthesizing answer with Ray Serve LLM...")
        logger.info("Request completed successfully. Latency: 450ms")

    logger.info("Simulation complete.")

if __name__ == "__main__":
    simulate_enterprise_activity()
