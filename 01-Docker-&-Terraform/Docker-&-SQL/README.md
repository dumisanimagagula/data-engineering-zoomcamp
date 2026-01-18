# NYC Yellow Taxi Ingestion

This is a configuration-driven ingestion pipeline that loads NYC Yellow Taxi data into PostgreSQL. Instead of passing command-line arguments, you modify a single YAML configuration file to control what data gets ingested.

## Two Ingestion Modes

### 1. Single Month (Default)
Ingest one month at a time:
```bash
python ingest_nyc_taxi_data.py
```

### 2. Batch Multiple Months (New!)
Ingest multiple months/years in one run:
```bash
python ingest_nyc_taxi_data.py --config config.examples/batch_2021_full_year.yaml
```

See [BATCH_INGESTION.md](BATCH_INGESTION.md) for details.

## Configuration-Driven Approach

The entire pipeline is controlled by configuration files: **`config.yaml`** or **`config_batch.yaml`**

### Quick Start: Ingest Different Data

**Single Month:**
```yaml
data_source:
  year: 2021        # ← Change year here
  month: 1          # ← Change month here (1-12)
  taxi_type: yellow # ← or change taxi type
```

**Multiple Months:**
```yaml
data_source:
  base_url: "https://..."
  taxi_type: yellow

data_sources:
  - year: 2021
    month: 1
  - year: 2021
    month: 2
  - year: 2021
    month: 3
```

Then run:
```bash
python ingest_nyc_taxi_data.py
```

Or with Docker Compose (prebuilt image + one-off runs):
```bash
# Build the ingestor image once
docker compose build ingestor

# Keep DB and pgAdmin running
docker compose up -d pgdatabase pgadmin

# Run ingestion with default config (config.yaml)
docker compose run --rm ingestor

# Run ingestion with a specific config
docker compose run --rm -e CONFIG_PATH=config.examples/batch_2021_q1.yaml ingestor
```

That's it! No more command-line arguments to remember.

## Configuration File Structure

`config.yaml` contains all settings:

```yaml
# Data source configuration (single month)
data_source:
  year: 2021                    # Year to ingest
  month: 1                      # Month (1-12)
  base_url: "https://d37ci6..."# Base URL for taxi data
```

# Database configuration
database:
  connection_string: "postgresql://root:root@localhost:5432/ny_taxi"
  table_name: "yellow_tripdata" # Table name

# Ingestion parameters
ingestion:
  chunk_size: 250000           # Rows per batch (optimized)
  n_jobs: 1                    # Parallel jobs (future)
  drop_existing: false         # Drop table first?
  if_exists: "replace"         # replace or append

# Logging
logging:
  level: "INFO"                # Log level
  file: ""                     # Log file path (optional)
```

## Run Locally
1) Install deps (prefer venv):
```bash
pip install -r requirements.txt
```

2) Edit `config.yaml` to choose year/month

3) Run ingestion:
```bash
python ingest_nyc_taxi_data.py
```

4) Or specify a different config file:
```bash
python ingest_nyc_taxi_data.py --config path/to/config.yaml
```

5) Run tests:
```bash
pytest
```

## Run with Docker Compose
Brings up PostgreSQL and pgAdmin, and supports on-demand ingestion runs:

```bash
# Build ingestor once
docker compose build ingestor

# Start core services
docker compose up -d pgdatabase pgadmin

# Run ingestion with default config
docker compose run --rm ingestor

# Run ingestion with a specific config
docker compose run --rm -e CONFIG_PATH=config.examples/prod.yaml ingestor
```

The ingestor reads `CONFIG_PATH` (defaulting to `config.yaml`) at runtime.

pgAdmin: http://localhost:8085 (email `admin@admin.com`, password `root`).

## Advantages of Configuration-Driven Design
- **Single source of truth**: All parameters in one file
- **No CLI argument confusion**: No need to remember flags or defaults
- **Easy templating**: Copy and modify config.yaml for different scenarios
- **Reproducibility**: Config file documents exactly what was ingested
- **Version control friendly**: Track config changes in git
- **Extensibility**: Easy to add new parameters without CLI changes

## Data Source & Engine
- Files: `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet`
- Key columns: `VendorID`, `passenger_count`, `trip_distance`, `PULocationID`, `DOLocationID`, `fare_amount`, `tip_amount`, `total_amount`, `tpep_pickup_datetime`, `tpep_dropoff_datetime`, etc.
- Parquet files are read via Polars (fast, vectorized); CSV fallback converts to Polars.
- Data is inserted using PostgreSQL COPY via `psycopg2` (much faster than `pandas.to_sql`).
- Schema is inferred from Polars dtypes; table is created on the first chunk.

## Example Workflows

### Single Month Workflows

**Ingest 2020 December data:**
```yaml
data_source:
  year: 2020
  month: 12
database:
  table_name: "yellow_tripdata_2020_12"
```

**Append to existing table instead of replacing:**
```yaml
ingestion:
  if_exists: "append"
```

**Increase chunk size for faster ingestion:**
```yaml
ingestion:
  chunk_size: 500000
```

### Batch Workflows (Multiple Months)

**Load Q1 2021:**
```bash
python ingest_nyc_taxi_data.py --config config.examples/batch_2021_q1.yaml
```

**Load full year 2021:**
```bash
python ingest_nyc_taxi_data.py --config config.examples/batch_2021_full_year.yaml
```

**Load multiple years:**
```bash
python ingest_nyc_taxi_data.py --config config.examples/batch_multi_year.yaml
```

See [BATCH_INGESTION.md](BATCH_INGESTION.md) for more batch examples and configuration details.
````
