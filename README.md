# Belgian Electricity Load Forecasting

Hourly forecasting of Belgium's electricity consumption, fully self-hosted with no cloud services and no managed data platform.

This is a portfolio project. The goal is to build the full data and MLOps lifecycle by hand, from raw ingestion to a served model, on infrastructure I run myself. It is not a production service.

## Status

The data pipeline is complete and running: ingestion from two public APIs and storage in a TimescaleDB time-series database. Feature engineering is the next step, followed by modeling and serving. Full roadmap below.

## Stack

- Python 3.12
- PostgreSQL 17 with the TimescaleDB 2.18 extension
- Docker Compose
- psycopg 3, pandas, numpy, requests
- Data sources: Energy-Charts API (Fraunhofer ISE), Open-Meteo

## Data pipeline

Two stages are implemented so far.

**Ingestion.** Belgian hourly load is pulled from the Energy-Charts API (Fraunhofer ISE, keyless). Weather is pulled from Open-Meteo. The ingestion layer only fetches and parses. It does not deduplicate or transform, which keeps it independent from how the data is stored.

**Storage.** Data lands in PostgreSQL 17 with the TimescaleDB extension, running in Docker. Load and weather observations share a single narrow table:

```sql
observations(
  ts     TIMESTAMPTZ,
  series TEXT,
  value  DOUBLE PRECISION,
  UNIQUE(ts, series)
)
```

stored as a TimescaleDB hypertable partitioned on `ts`. A few design decisions:

- Everything is stored in UTC. Local Belgian time is derived later, at feature-engineering time, so the raw data carries no timezone ambiguity.
- Writes are idempotent. Re-running ingestion over a period that already exists updates rows in place (`ON CONFLICT (ts, series) DO UPDATE`) rather than duplicating them, so the pipeline is safe to re-run.
- Deduplication lives in the storage layer, enforced by the unique constraint, not in the ingestion code.

## Architecture

```
Energy-Charts API ─┐
(Belgian load)     │
                   ├─▶ ingestion ─▶ TimescaleDB ─▶ features ─▶ model ─▶ serving
Open-Meteo ────────┘   fetch/parse    (UTC)
(weather)              [done]         [done]       [next]     [planned] [planned]
```

## Roadmap

The project is organized as 10 modules covering the full lifecycle.

- [X] 0. Project setup and Git
- [X] 1. Ingestion
- [X] 2. Storage (TimescaleDB)
- [ ] 3. Feature engineering
- [ ] 4. Modeling and experiment tracking (MLflow)
- [ ] 5. Serving (FastAPI)
- [ ] 6. Monitoring
- [ ] 7. Orchestration and CI/CD
- [ ] 8. Containerization (k3s)
- [ ] 9. Hardening and GDPR

## Running it

Requirements: Docker with Docker Compose, and Python 3.12.

1. Set `POSTGRES_PASSWORD` in a `.env` file at the repository root (see `compose.yaml`).
2. Start the database: `docker compose up -d`
3. Create and activate a virtual environment, then install dependencies: `pip install -r requirements.txt`
4. Apply the schema in `schema.sql`, then run :
   ```
   python -m src.ingestion.weather
   python -m src.ingestion.load
   python -m src.storage.load_to_db
   ```

## Data sources and licensing

- Electricity load: Energy-Charts API by Fraunhofer ISE. Data licensed under CC BY 4.0, attribution to Energy-Charts.info. No API key required.
- Weather: Open-Meteo. Data licensed under CC BY 4.0, free tier for non-commercial use, attribution to Open-Meteo.com. No API key required.
