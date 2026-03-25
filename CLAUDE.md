# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Database

Postgres 16 running in Docker. Start/stop with:

```bash
docker compose up -d        # start (preserves data)
docker compose down         # stop (preserves data)
docker compose down -v      # full reset — reruns data load on next startup
```

Connect via psql:
```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

Connection string: `postgresql://postgres:postgres@localhost:5432/campus_bites`

## Data Loading

**`load_data.py`** (root level) — Python script using `psycopg2` + stdlib `csv`. Truncates and reloads all rows on every run. Run with:

```bash
.venv/Scripts/python.exe load_data.py
```

The `campus-bites-pipeline/` subdirectory contains an older SQL-based approach (`init.sql`) that loads via Postgres's `COPY` command on first container startup. The root-level `docker-compose.yml` no longer uses this approach. The CSV lives at `data/campus_bites_orders.csv`.

## Python Environment

The venv is at `.venv/`. The system `python` and `python3` commands are Windows Store stubs — always use the venv interpreter explicitly:

```bash
.venv/Scripts/python.exe         # run scripts
.venv/Scripts/pip install <pkg>  # install packages
source .venv/Scripts/activate    # or activate the venv
```

The venv was created from Anaconda Python at `C:/Users/chels/anaconda3/python.exe`.

## Schema Notes

The `orders` table (root setup) stores `promo_code_used` and `is_reorder` as `TEXT` (`'Yes'`/`'No'`). The `campus-bites-pipeline/init.sql` version casts these to `BOOLEAN` via a staging table — use that as a reference if the schema is ever migrated.

| Column | Type |
|--------|------|
| `order_id` | `INTEGER` PK |
| `order_date` | `DATE` |
| `order_time` | `TIME` |
| `customer_segment` | `TEXT` |
| `order_value` | `NUMERIC(10,2)` |
| `cuisine_type` | `TEXT` |
| `delivery_time_mins` | `INTEGER` |
| `promo_code_used` | `TEXT` (`'Yes'`/`'No'`) |
| `is_reorder` | `TEXT` (`'Yes'`/`'No'`) |
