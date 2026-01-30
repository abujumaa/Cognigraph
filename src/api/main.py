import os
import uvicorn
import time
import uuid
from fastapi import FastAPI, HTTPException, Request, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from src.agents.workflow import app as graph_app
from src.utils.logger import logger

# --- Security Setup ---
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validates the API Key. In a real enterprise app, check against a DB or Vault.
    """
    if os.getenv("ENV") == "development":
        return api_key_header # Allow anything in dev if needed, or enforce specific dev key

    expected_key = os.getenv("GRAPH_RAG_API_KEY", "secret-enterprise-key")
    if api_key_header == expected_key:
        return api_key_header
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# --- App Setup ---
app = FastAPI(
    title="CogniGraph API",
    description="Gateway for Hybrid Search using Neo4j and Qdrant",
    version="1.0.0"
)

# --- Middleware: Correlation ID ---
@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    # In a real logger, we would set this in the context var
    logger.info(f"Processing request {correlation_id} - Path: {request.url.path}")
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Correlation-ID"] = correlation_id
    logger.info(f"Completed request {correlation_id} - Duration: {process_time:.4f}s - Status: {response.status_code}")
    return response

# --- Models ---
class QueryRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None

class QueryResponse(BaseModel):
    answer: str
    execution_plan: Optional[str]

# --- Endpoints ---

@app.get("/health")
async def health_check():
    logger.debug("Health check requested")
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_system(
    request: QueryRequest, 
    api_key: str = Depends(get_api_key)
):
    """
    Main entry point for the RAG system.
    Orchestrates the query through the Multi-Agent Logic.
    Secured by API Key.
    """
    try:
        logger.info(f"Received query: {request.query}")
        # Run the LangGraph workflow
        initial_state = {"query": request.query, "vector_results": [], "graph_results": []}
        result = graph_app.invoke(initial_state)
        
        logger.info(f"Query processed successfully. Plan: {result.get('plan')}")
        return QueryResponse(
            answer=result.get("final_answer", "No answer generated."),
            execution_plan=result.get("plan")
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8080, reload=True)