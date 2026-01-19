# Dockerfile for NYC Taxi Data Ingestor
# Production-ready image with optimized layer caching

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config.yaml .
COPY config.examples/ ./config.examples/

# Set Python path to include src
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Default command
CMD ["python", "src/ingest_nyc_taxi_data.py", "--config", "config.yaml"]
