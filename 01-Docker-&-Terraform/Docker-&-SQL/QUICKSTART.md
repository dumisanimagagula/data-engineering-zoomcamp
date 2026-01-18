# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure (Edit ONE File)
Open `config.yaml` and change these lines to pick your month:
```yaml
data_source:
  year: 2021        # ← Change this
  month: 1          # ← Or this
```

### 3. Run
```bash
python ingest_nyc_taxi_data.py
```

Done! Your data is being ingested.

---

## For Different Months

Just change 2 numbers in `config.yaml`:

**Want 2020, December?**
```yaml
data_source:
  year: 2020
  month: 12
```

**Want 2021, June?**
```yaml
data_source:
  year: 2021
  month: 6
```

Then run: `python ingest_nyc_taxi_data.py`

---

## With Docker (Prebuilt + One-Off Runs)

```bash
# Build ingestor once
docker compose build ingestor

# Start database + pgAdmin (keeps running)
docker compose up -d pgdatabase pgadmin

# Run ingestion with default config
docker compose run --rm ingestor

# Run ingestion with a specific config
docker compose run --rm -e CONFIG_PATH=config.examples/batch_2021_q1.yaml ingestor
```

Notes:
- Use pgdatabase as the host in `connection_string` when running inside Docker.
- Use localhost as the host when running locally outside Docker.

---

## Key Concepts

**Old Way (Arguments):**
```bash
python script.py --year 2021 --month 1 --chunk-size 100000 --table yellow_taxi_data
```
Too many arguments!

**New Way (Config File):**
```bash
python script.py
```
Edit config.yaml once, run script with no arguments.

---

## Verify It Works

After running, check pgAdmin:
- URL: http://localhost:8085
- Email: admin@admin.com
- Password: root

Query the data:
```sql
SELECT COUNT(*) FROM yellow_tripdata;
SELECT * FROM yellow_tripdata LIMIT 5;
```

Indexes are created after ingestion completes for faster queries.

---

## Next Steps

- See [CONFIGURATION.md](CONFIGURATION.md) for all options
- See [README.md](README.md) for technical details
- See performance notes in [PERFORMANCE_OPTIMIZATIONS.md](PERFORMANCE_OPTIMIZATIONS.md)
- Run tests: `pytest`
