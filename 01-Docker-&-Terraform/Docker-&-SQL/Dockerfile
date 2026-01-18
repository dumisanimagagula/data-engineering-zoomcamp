# Dockerfile for NYC Taxi Data Ingestor
# Pre-builds dependencies to speed up container startup

FROM python:3.12-slim

# Set working directory
WORKDIR /code

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Default command (overridden by docker-compose)
CMD ["python", "ingest_nyc_taxi_data.py", "--config", "config.yaml"]
