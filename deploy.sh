#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting CogniGraph Deployment...${NC}"

# 1. Build the API Image
echo -e "${GREEN}Building API Docker Image...${NC}"
docker build -t cognigraph:latest .

# 2. Stop existing services
echo -e "${GREEN}Stopping existing services...${NC}"
docker-compose down

# 3. Start Infrastructure
echo -e "${GREEN}Starting services (Neo4j, Qdrant, Ray Serve, API)...${NC}"
docker-compose up -d --build

# 4. Wait for Health Check
echo -e "${GREEN}Waiting for API to be ready...${NC}"
echo "Sleeping for 10 seconds..."
sleep 10

HEALTH_URL="http://localhost:8080/health"
STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL || echo "000")

if [ "$STATUS_CODE" -eq 200 ]; then
    echo -e "${GREEN}Deployment Successful! 🚀${NC}"
    echo -e "API is running at: http://localhost:8080"
    echo -e "Neo4j Browser: http://localhost:7474 (user: neo4j, pass: password)"
    echo -e "Qdrant UI: http://localhost:6333/dashboard"
else
    echo -e "\033[0;31mDeployment might have issues. Health check returned: $STATUS_CODE${NC}"
    echo "Check logs with: docker-compose logs -f"
fi
