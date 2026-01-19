# NYC Taxi Data Ingestion Pipeline

Production-ready, config-driven data ingestion pipeline for NYC Yellow Taxi trip data and zone reference data into PostgreSQL.

## Features

- ✅ **Config-Driven**: All settings in YAML - no hardcoded values
- ✅ **Batch Processing**: Ingest single or multiple months in one run
- ✅ **Zone Integration**: Automatic zones reference data ingestion
- ✅ **High Performance**: Optimized with PostgreSQL COPY and chunked processing
- ✅ **Docker Ready**: Containerized with Docker Compose orchestration
- ✅ **Production Ready**: Clean structure, comprehensive documentation

## Quick Start

### 1. Start Services
```bash
docker compose up -d pgdatabase pgadmin
```

### 2. Configure Ingestion

Edit `config.yaml` or use existing examples:

```yaml
# Single month
data_source:
  year: 2021
  month: 1
  taxi_type: yellow

# Enable zones (optional)
zones:
  enabled: true
```

### 3. Run Ingestion

```bash
# Default config
docker compose run --rm ingestor

# Specific config
docker compose run --rm -e CONFIG_PATH=config.examples/batch_2021_q1.yaml ingestor

# Zones only
docker compose run --rm -e CONFIG_PATH=config.examples/zones_only.yaml ingestor python src/ingest_zones.py
```

## Project Structure

```
├── src/                          # Source code
│   ├── ingest_nyc_taxi_data.py  # Main ingestion script
│   ├── ingest_zones.py          # Zones ingestion script
│   └── config_loader.py         # Configuration parser
├── config.examples/             # Example configurations
│   ├── batch_2021_q1.yaml       # Q1 2021 batch
│   ├── batch_2021_full_year.yaml # Full year 2021
│   ├── batch_2025_full_year.yaml # Full year 2025
│   ├── with_zones.yaml          # Single month + zones
│   └── zones_only.yaml          # Zones only
├── docs/                        # Documentation
│   ├── BATCH_INGESTION.md       # Batch processing guide
│   ├── CONFIGURATION.md         # Configuration reference
│   ├── CONFIG_EXAMPLES.md       # Config examples
│   ├── ZONES_README.md          # Zones data guide
│   └── QUICK_REFERENCE.md       # Command reference
├── scripts/                     # Utility scripts
│   ├── verify_zones.py          # Verify zones data
│   ├── example_zones_join.py    # Example queries
│   └── test_config_driven.py    # Integration test
├── docker-init-scripts/         # PostgreSQL init scripts
├── config.yaml                  # Default configuration
├── docker-compose.yaml          # Docker orchestration
├── Dockerfile                   # Production image
└── requirements.txt             # Python dependencies
```

## Configuration

### Basic Configuration

```yaml
# Data source
data_source:
  year: 2021
  month: 1
  base_url: "https://d37ci6vzurychx.cloudfront.net/trip-data"
  taxi_type: yellow

# Database
database:
  connection_string: "postgresql://root:root@pgdatabase:5432/ny_taxi"
  table_name: "yellow_tripdata"

# Ingestion
ingestion:
  chunk_size: 250000
  drop_existing: false
  if_exists: "replace"

# Zones (optional)
zones:
  enabled: true
  table_name: "zones"
  create_index: true
```

### Batch Ingestion

```yaml
data_source:
  base_url: "https://d37ci6vzurychx.cloudfront.net/trip-data"
  taxi_type: yellow

data_sources:
  - year: 2021
    month: 1
  - year: 2021
    month: 2
  - year: 2021
    month: 3
```

See [docs/CONFIG_EXAMPLES.md](docs/CONFIG_EXAMPLES.md) for more examples.

## Usage Examples

### Ingest Single Month
```bash
docker compose run --rm ingestor
```

### Ingest Q1 2021
```bash
docker compose run --rm -e CONFIG_PATH=config.examples/batch_2021_q1.yaml ingestor
```

### Ingest Full Year 2025
```bash
docker compose run --rm -e CONFIG_PATH=config.examples/batch_2025_full_year.yaml ingestor
```

### Ingest Zones Only
```bash
docker compose run --rm -e CONFIG_PATH=config.examples/zones_only.yaml ingestor python src/ingest_zones.py
```

### Verify Zones Data
```bash
docker compose run --rm ingestor python scripts/verify_zones.py
```

## Access Services

- **pgAdmin**: http://localhost:8085
  - Email: admin@admin.com
  - Password: root

- **PostgreSQL**: localhost:5432
  - User: root
  - Password: root
  - Database: ny_taxi

## Performance

- **Chunk Size**: 250,000 rows per batch (optimized for COPY)
- **Method**: PostgreSQL COPY for high-speed bulk inserts
- **Indexing**: Automatic index creation after ingestion
- **Schema Fixes**: Automatic datetime column type conversion

## Data Sources

- **Trip Data**: https://d37ci6vzurychx.cloudfront.net/trip-data/
- **Zones Data**: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv

## Documentation

- [BATCH_INGESTION.md](docs/BATCH_INGESTION.md) - Batch processing guide
- [CONFIGURATION.md](docs/CONFIGURATION.md) - Advanced configuration
- [ZONES_README.md](docs/ZONES_README.md) - Zones reference data
- [QUICK_REFERENCE.md](docs/QUICK_REFERENCE.md) - Command quick reference

## Requirements

- Docker & Docker Compose
- 2GB+ RAM for database
- Network access to data sources

## Development

### Local Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally (update connection string in config.yaml)
python src/ingest_nyc_taxi_data.py --config config.yaml
```

### Rebuild Image
```bash
docker compose build ingestor
```

## Troubleshooting

### Schema Mismatch
If ingesting different years with different schemas:
```bash
# Clean database
docker compose down -v

# Run ingestion
docker compose run --rm -e CONFIG_PATH=your_config.yaml ingestor
```

### Check Logs
```bash
docker compose logs pgdatabase
docker compose logs ingestor
```

## License

MIT
