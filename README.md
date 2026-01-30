# CogniGraph: Enterprise GraphRAG System

## Overview
This project implements an **Enterprise-grade GraphRAG** (Retrieval-Augmented Generation) system. It utilizes a **Hybrid Search** architecture that combines the semantic power of **Vector Databases** (Qdrant) with the relational reasoning of **Graph Databases** (Neo4j).

The system is orchestrated using **LangGraph** to manage a multi-agent workflow that plans, searches, and synthesizes answers.

## 🚀 Use Cases

1.  **Complex Multi-Hop Reasoning**:
    *   *Scenario*: "How is the Director of Engineering related to project Alpha's deadline?"
    *   *Solution*: The **Graph Searcher** traverses organizational and project relationships in Neo4j to find the connection.

2.  **Semantic Information Retrieval**:
    *   *Scenario*: "Find all policy documents regarding remote work."
    *   *Solution*: The **Vector Searcher** uses Qdrant to find semantically similar text chunks even if keywords don't match exactly.

3.  **Hybrid Enterprise Search**:
    *   *Scenario*: "What are the risks associated with the vendors mentioned in the Q3 audit report?"
    *   *Solution*: The **Planner Agent** breaks this down: Vector search finds the "Q3 audit report", while Graph search identifies "vendors" and their linked "risk" entities.

## 📂 Project Structure

```text
.
├── config/                 # Configuration files
├── docker-compose.yml      # Infrastructure (Neo4j, Qdrant, Ray Serve)
├── pyproject.toml          # Dependencies (Poetry)
├── src/
│   ├── agents/             # LangGraph Multi-Agent Logic
│   │   ├── planner.py      # Decides execution strategy (Vector/Graph/Hybrid)
│   │   ├── graph_search.py # Neo4j interaction
│   │   ├── vector_search.py# Qdrant interaction
│   │   └── workflow.py     # Graph definition
│   ├── api/                # FastAPI Gateway
│   ├── ingestion/          # Data pipeline (S3 -> Qdrant + Neo4j)
│   └── llm/                # Ray Serve / VLLM Client
└── tests/                  # Unit and Integration tests
```

## 🛠️ Setup & Installation

### Prerequisites
*   Python 3.9+
*   Docker & Docker Compose (for the databases)

### 1. Environment Setup
Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
# OR if using Poetry
poetry install
```
*(Note: Ensure you have `fastapi`, `uvicorn`, `langgraph`, `neo4j`, `qdrant-client`, etc., installed).*

## 🏃‍♂️ How to Run

### Step 1: Start Infrastructure (Databases)
Spin up Neo4j, Qdrant, and Ray Serve using Docker:
```bash
docker-compose up -d
```
*If you do not have Docker, the agents are currently configured with **Mock** fallbacks for demonstration purposes.*

### Step 2: Run the API Server
Start the FastAPI gateway:
```bash
export PYTHONPATH=$PYTHONPATH:.
# Optional: Set API Key
export GRAPH_RAG_API_KEY="my-secret-key"
python src/api/main.py
```
The server will start at `http://0.0.0.0:8080`.

## 🔒 Security
The API is secured with an API Key.
*   **Header**: `X-API-Key`
*   **Default (Dev)**: No auth required if `ENV=development`
*   **Production**: Set `GRAPH_RAG_API_KEY` env var.

## 🐳 Docker Build
To build the API container manually:
```bash
docker build -t enterprise-graphrag .
```

## 📖 User Guide

This guide will walk you through the end-to-end usage of the Enterprise GraphRAG system, from ingestion to complex querying and monitoring.

### 1. Authentication
In a production environment, you must include the API Key in your requests.
*   **Header Name**: `X-API-Key`
*   **Value**: Your configured secret (default: `secret-enterprise-key`)

**Example Header:**
```bash
-H "X-API-Key: secret-enterprise-key"
```

### 2. Ingesting Data 📥
Before querying, populate your databases (Neo4j & Qdrant) with enterprise data.
1.  Ensure Docker services are running (`docker-compose up -d`).
2.  Run the pipeline script:
    ```bash
    PYTHONPATH=. python src/ingestion/pipeline.py
    ```
    *This script currently mocks fetching from S3, chunks the text, and performs dual-ingestion.*

### 3. Querying the System 🔍
You can interact with the API using `curl`, Postman, or any HTTP client.

#### A. Health Check
Ensure all services are operational.
```bash
curl -X GET http://localhost:8080/health
```

#### B. Natural Language Query
The system automatically routes your query to the best search engine (Vector, Graph, or Both).

**Example 1: Unstructured Search (Vector)**
*Intent: Finding documents based on semantic content.*
```bash
curl -X POST http://localhost:8080/query \
     -H "Content-Type: application/json" \
     -H "X-API-Key: secret-enterprise-key" \
     -d '{"query": "Find all summaries related to the 2024 financial outlook."}'
```

**Example 2: Relationship Search (Graph)**
*Intent: Traversing entities and relationships.*
```bash
curl -X POST http://localhost:8080/query \
     -H "Content-Type: application/json" \
     -H "X-API-Key: secret-enterprise-key" \
     -d '{"query": "How is Director Alice related to the Project Apollo delay?"}'
```

**Example 3: Hybrid Search (Complex)**
*Intent: Combining specific documents with entity knowledge.*
```bash
curl -X POST http://localhost:8080/query \
     -H "Content-Type: application/json" \
     -H "X-API-Key: secret-enterprise-key" \
     -d '{"query": "What risks are listed in the Q3 audit report regarding Vendor X?"}'
```

### 4. Monitoring & Logs 📊
The system logs detailed execution traces to help you understand the Planner's decisions and performance.

*   **Application Log**: `logs/app.log` (General usage stats)
*   **Debug Log**: `logs/debug.log` (Detailed agent reasoning and step-by-step traces)
*   **Error Log**: `logs/error.log` (Critical failures)

**View live logs:**
```bash
tail -f logs/app.log
```

## 🧠 System Architecture details

1.  **Ingestion**: `src/ingestion/pipeline.py` fetches data (mocked S3), chunks text, generates embeddings for **Qdrant**, and extracts entities/relationships for **Neo4j**.
2.  **API Gateway**: Receives the user request.
3.  **Planner Agent**: Uses an LLM to classify the intent (`vector`, `graph`, or `hybrid`).
4.  **Routing**:
    *   **Vector Node**: Queries Qdrant for semantic similarity.
    *   **Graph Node**: Generates Cypher queries to traverse Neo4j.
5.  **Synthesizer**: Aggregates context from both streams and uses an LLM (Ray Serve) to generate the final natural language response.

## ✅ Testing
Run the test suite to verify agent logic and API endpoints:
```bash
PYTHONPATH=. pytest tests
```
