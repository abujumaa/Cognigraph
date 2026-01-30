# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies (e.g., for Neo4j driver or compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (optional, if using pyproject.toml directly) or just pip
# Here we stick to standard pip for simplicity in the container, 
# converting the pyproject.toml concepts to requirements or just installing dependencies.
# We will use the requirements.txt generated earlier.

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src
COPY config/ ./config

# Expose port
EXPOSE 8080

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "src/api/main.py"]
