# Configuration-Driven Ingestion System - Implementation Summary

## What Was Changed

This project has been refactored to use a **configuration-driven approach** instead of command-line arguments. Users now modify a single `config.yaml` file to control ingestion parameters.

## Files Changed/Created

### Modified Files
1. **ingest_nyc_taxi_data.py**
   - Removed all CLI arguments (`--year`, `--month`, `--pg-user`, etc.)
   - Added single `--config` option pointing to YAML file
   - Updated to use `Config` class from `config_loader`
   - Refactored to handle both parquet and CSV files

2. **docker-compose.yaml**
   - Simplified command to just read `config.yaml`
   - Removed environment variable overrides (now in config file)

3. **requirements.txt**
   - Added `pyyaml==6.0.1` for YAML parsing

### New Files
1. **config.yaml**
   - Main configuration file (what users edit)
   - Includes: data source, database, ingestion, logging settings

2. **config_loader.py**
   - Config file parser
   - Dataclasses for configuration validation
   - Auto-generates data URLs from year/month/taxi_type

3. **README.md**
   - Updated with configuration-driven approach
   - Shows simple examples

4. **CONFIGURATION.md**
   - Comprehensive guide to all config options
   - Explains the pattern and benefits
   - Common workflows and examples

5. **QUICKSTART.md**
   - 5-minute getting started guide
   - Shows how to change month and run

6. **config.examples/**
   - `dev.yaml` - Development setup (small chunks)
   - `prod.yaml` - Production setup (large chunks, append mode)
   - `bulk.yaml` - One-time bulk import (very large chunks)
   - `archive.yaml` - Monthly archive (append to growing table)

## How It Works

### Configuration Flow
```
config.yaml
    ↓
Config.from_file() [config_loader.py]
    ↓
Config object (with validation)
    ↓
ingest_nyc_taxi_data.py uses config
    ↓
Data ingestion
```

### User Experience

**Before:**
```bash
python ingest_nyc_taxi_data.py --year 2021 --month 3 --chunk-size 100000 \
  --pg-user root --pg-password root --pg-host localhost --pg-port 5432 \
  --pg-db ny_taxi --table-name yellow_tripdata
```

**After:**
```yaml
# Edit config.yaml:
data_source:
  year: 2021
  month: 3
ingestion:
   chunk_size: 250000
# ... rest of config

# Then run:
python ingest_nyc_taxi_data.py
```

## Key Features

### 1. Automatic URL Generation
Config contains:
```yaml
data_source:
  year: 2021
  month: 1
  taxi_type: yellow
  base_url: "https://..."
```

Script auto-generates: `https://.../yellow_tripdata_2021-01.parquet`

### 2. Configuration Validation
- Config file parsed as YAML
- Dataclasses validate required fields
- Type checking built-in
- Clear error messages if config is invalid

### 3. Flexible File Formats
Script automatically detects and handles:
- Parquet files (`.parquet`) via Polars (fast, vectorized)
- CSV/Gzip files (`.csv.gz`) with a CSV fallback converted to Polars
- Both support chunked reading and high-throughput COPY inserts

### 4. Multiple Configurations
Use different configs for different scenarios:
```bash
python ingest_nyc_taxi_data.py --config config.examples/dev.yaml
python ingest_nyc_taxi_data.py --config config.examples/prod.yaml
python ingest_nyc_taxi_data.py --config config.examples/archive.yaml
```

## Benefits

### For Users
- ✅ Clear: One file to edit
- ✅ Reproducible: Config documents what was ingested
- ✅ Safe: Hard to make CLI argument mistakes
- ✅ Discoverable: All options listed in config file

### For Teams
- ✅ Consistent: Everyone uses same config format
- ✅ Auditable: Git history shows all config changes
- ✅ Shareable: Easy to copy configs between environments
- ✅ Scriptable: Orchestrators can read YAML configs

### For Operations
- ✅ Scalable: Easy to add new parameters
- ✅ Maintainable: No long command lines to manage
- ✅ Monitored: Config changes are version controlled
- ✅ Templatable: Create configs from templates

## Common Use Cases

### 1. Monthly Data Pipeline
```yaml
# January
data_source:
  month: 1
# ... run ingest

# February
data_source:
  month: 2
# ... run ingest
```

### 2. Multi-Environment
```bash
# Local testing
python ingest.py --config config.examples/dev.yaml

# Production
python ingest.py --config config.examples/prod.yaml
```

### 3. Historical Bulk Load
```bash
python ingest.py --config config.examples/bulk.yaml
```

### 4. Growing Archive
```bash
# Keep appending new months
python ingest.py --config config.examples/archive.yaml
# Change month, run again, data appends
```

## Testing

All existing tests continue to work. The configuration system is separate from core ingestion logic.

```bash
pytest
```

## Migration Guide (If You Had CLI Args)

### Before
```bash
python ingest.py --year 2021 --month 1
```

### After
```yaml
# config.yaml
data_source:
  year: 2021
  month: 1
```
```bash
python ingest.py
```

## Future Extensions

This config-driven approach makes it easy to add:
- Data validation rules
- Transformation pipelines
- Notification settings
- Performance tuning options
- Multi-source ingestion
- Scheduled executions

Just add to config.yaml and update `config_loader.py` and `ingest_nyc_taxi_data.py`.

## Architecture Pattern

This follows the **configuration-driven design pattern** used by:
- Azure Data Factory (JSON pipelines)
- Apache Airflow (DAG configurations)
- Terraform (HCL configs)
- Docker Compose (YAML configs)

Benefits include:
- Separation of logic from configuration
- Version control of pipelines
- Easy orchestration and scheduling
- Clear audit trails
