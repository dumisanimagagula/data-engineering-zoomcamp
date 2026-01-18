# Configuration Examples

This directory contains example configurations for different scenarios.

## Usage

Copy any example config to `config.yaml`:

```bash
cp config.examples/prod.yaml config.yaml
python ingest_nyc_taxi_data.py
```

Or specify the config explicitly:

```bash
python ingest_nyc_taxi_data.py --config config.examples/prod.yaml
```

## Example Scenarios

### 1. Local Development (`dev.yaml`)
- Uses local PostgreSQL
- Imports single month
- Small chunk size for testing

### 2. Production (`prod.yaml`)
- Uses production PostgreSQL instance
- Larger chunk size for performance
- Appends data instead of replacing

### 3. Historical Bulk Load (`bulk.yaml`)
- Large chunk size (1M rows)
- Optimized for one-time bulk import
- Replaces existing data

### 4. Remote Database (`remote.yaml`)
- Connects to cloud PostgreSQL
- Uses SSL for security
- Configured for cloud performance

### 5. Archive (`archive.yaml`)
- Appends to archive table
- Uses separate naming convention
- Preserves historical data
