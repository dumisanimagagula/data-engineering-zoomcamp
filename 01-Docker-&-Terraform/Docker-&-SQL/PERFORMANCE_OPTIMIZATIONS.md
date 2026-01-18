# Performance Optimizations

## Overview
This project uses Polars for fast parquet reads and PostgreSQL COPY via psycopg2 for high-throughput inserts. The ingestor image is prebuilt to avoid per-run dependency installation. PostgreSQL parameters are tuned for bulk loads.

## Key Changes
- Polars-based reads (parquet) and conversion for CSV fallback
- COPY FROM STDIN inserts via `psycopg2` (faster than `pandas.to_sql`)
- Deferred index creation until after ingestion completes
- Reduced validation sampling and log volume
- Prebuilt Docker image to eliminate runtime `pip install`
- PostgreSQL tuning (e.g., `shared_buffers`, `work_mem`, `maintenance_work_mem`, WAL settings)

## Recommended Settings
- `ingestion.chunk_size`: 250k by default; increase to 500k–1M for bulk loads if memory allows.
- Run database and pgAdmin via `docker compose up -d pgdatabase pgadmin`, then trigger one-off ingestions with `CONFIG_PATH`.
- Use `if_exists: append` for batch loads and `replace` when initializing a fresh table.

## Docker Workflow
```bash
# Build ingestor once
docker compose build ingestor

# Start DB services
docker compose up -d pgdatabase pgadmin

# One-off ingestion with specific config
docker compose run --rm -e CONFIG_PATH=config.examples/batch_2021_q1.yaml ingestor
```

## Notes
- Inside Docker, set database host to `pgdatabase`; outside Docker, use `localhost`.
- Indexes are created after ingestion to accelerate queries without slowing inserts.
