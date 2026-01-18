# 📚 Getting Started Guide

## 🚀 Quick Start (2 Minutes)

### 1. Edit `config.yaml`
Change the year and month you want to ingest:

```yaml
data_source:
  year: 2021    # ← Your year
  month: 1      # ← Your month (1-12)
```

### 2. Run
```bash
python ingest_nyc_taxi_data.py
```

Done! Your data is being ingested.

---

## 📖 Documentation (Pick What You Need)

### Just Starting Out?
👉 Read **[SUMMARY.md](SUMMARY.md)** (2 minutes)
- Overview of the new approach
- What changed
- Key benefits

### Need a Quick Tutorial?
👉 Read **[QUICKSTART.md](QUICKSTART.md)** (5 minutes)
- How to use the system
- Common tasks
- Docker setup

### Want All Configuration Options?
👉 Read **[CONFIGURATION.md](CONFIGURATION.md)** (10 minutes)
- All configuration parameters
- Examples for different scenarios
- Troubleshooting

### Interested in Technical Details?
👉 Read **[IMPLEMENTATION.md](IMPLEMENTATION.md)** (15 minutes)
- How the system was implemented
- Architecture and design decisions
- Extending the system

### Looking for Examples?
👉 Check **[config.examples/](config.examples/)** folder
- `dev.yaml` - Development setup
- `prod.yaml` - Production setup
- `bulk.yaml` - Bulk import setup
- `archive.yaml` - Archive/append setup

---

## 🎯 Common Tasks

### Change the Month
Edit `config.yaml`:
```yaml
data_source:
  month: 3  # Changed from 1 to 3
```

### Use a Different Database
Edit `config.yaml`:
```yaml
database:
  connection_string: "postgresql://user:pass@host:5432/database"
```

### Append Instead of Replace
Edit `config.yaml`:
```yaml
ingestion:
  if_exists: "append"
```

### Use Development Settings
```bash
python ingest_nyc_taxi_data.py --config config.examples/dev.yaml
```

### Use Production Settings
```bash
python ingest_nyc_taxi_data.py --config config.examples/prod.yaml
```

### Run with Docker
```bash
# Build ingestor once
docker compose build ingestor

# Start DB + pgAdmin
docker compose up -d pgdatabase pgadmin

# Run ingestion (default config)
docker compose run --rm ingestor

# Run ingestion (specific config)
docker compose run --rm -e CONFIG_PATH=config.examples/batch_2021_q1.yaml ingestor
```

---

## 🧪 Testing

### Test Config Loading
```bash
python -c "from config_loader import Config; cfg = Config.from_file('config.yaml'); print(f'URL: {cfg.data_source.url}')"
```

### Run Tests
```bash
pytest
```

---

## ❓ FAQ

**Q: How do I change what month gets ingested?**
A: Edit `config.yaml` and change `data_source.month`. See QUICKSTART.md.

**Q: Can I use different configs for different environments?**
A: Yes! Use `--config` flag or check `config.examples/` folder.

**Q: What if my config file is invalid?**
A: The script will show an error. Check CONFIGURATION.md for valid options.

**Q: Can I still use command-line arguments?**
A: No, the system is now config-driven. Edit `config.yaml` instead.

**Q: How do I schedule ingestions?**
A: Use a scheduler (cron, Airflow, etc.) to run `python ingest_nyc_taxi_data.py`.

---

## 📋 File Structure

```
project/
├── config.yaml                  ← EDIT THIS
├── config_loader.py             ← Do not edit
├── ingest_nyc_taxi_data.py      ← Do not edit
├── config.examples/
│   ├── dev.yaml
│   ├── prod.yaml
│   ├── bulk.yaml
│   └── archive.yaml
├── SUMMARY.md                   ← Start here
├── QUICKSTART.md
├── CONFIGURATION.md
├── IMPLEMENTATION.md
└── README.md
```

---

## 🎓 Learning Path

**Complete Beginner:**
1. Read SUMMARY.md (2 min)
2. Read QUICKSTART.md (5 min)
3. Edit config.yaml
4. Run: `python ingest_nyc_taxi_data.py`
5. Check pgAdmin at localhost:8085

**Experienced User:**
1. Skim SUMMARY.md (1 min)
2. Check config.examples/ (2 min)
3. Copy desired config: `cp config.examples/prod.yaml config.yaml`
4. Edit config.yaml as needed
5. Run: `python ingest_nyc_taxi_data.py`

**Developer:**
1. Read IMPLEMENTATION.md (15 min)
2. Review config_loader.py
3. Review changes in ingest_nyc_taxi_data.py
4. Understand the architecture

---

## 🔗 Quick Links

- **Make changes**: Edit `config.yaml`
- **Run locally**: `python ingest_nyc_taxi_data.py`
- **Run with Docker**: `docker compose build ingestor && docker compose up -d pgdatabase pgadmin && docker compose run --rm ingestor`
- **View database**: http://localhost:8085 (pgAdmin)
- **Run tests**: `pytest`

---

## ✨ That's It!

The system is designed to be simple and intuitive:

1. **One config file** - `config.yaml`
2. **One command** - `python ingest_nyc_taxi_data.py`
3. **That's it!** - No complicated arguments

Happy ingesting! 🎉
