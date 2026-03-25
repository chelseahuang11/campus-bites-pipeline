# Campus Bites — Local Postgres Setup

A local Postgres database preloaded with Campus Bites order data, running in Docker.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

## Quick Start

```bash
docker compose up -d
```

That's it. On first run, Docker will:
1. Pull the Postgres 16 image
2. Create the `campus_bites` database
3. Create the `orders` table
4. Load all data from `campus-bites-pipeline/data/campus_bites_orders.csv`

## Connection Details

| Setting  | Value          |
|----------|----------------|
| Host     | `localhost`    |
| Port     | `5432`         |
| Database | `campus_bites` |
| User     | `postgres`     |
| Password | `postgres`     |

## Connecting

### psql (command line)

```bash
docker exec -it campus_bites_db psql -U postgres -d campus_bites
```

### GUI Client (DBeaver, TablePlus, etc.)

Create a new PostgreSQL connection using the connection details above.

### Connection String

```
postgresql://postgres:postgres@localhost:5432/campus_bites
```

## Sample Queries

```sql
-- Preview the data
SELECT * FROM orders LIMIT 10;

-- Orders by cuisine type
SELECT cuisine_type, COUNT(*) AS total_orders, ROUND(AVG(order_value), 2) AS avg_value
FROM orders
GROUP BY cuisine_type
ORDER BY total_orders DESC;

-- Reorder rate by customer segment
SELECT customer_segment,
       COUNT(*) AS total,
       SUM(CASE WHEN is_reorder = 'Yes' THEN 1 ELSE 0 END) AS reorders,
       ROUND(100.0 * SUM(CASE WHEN is_reorder = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS reorder_pct
FROM orders
GROUP BY customer_segment;
```

## Stopping the Database

```bash
# Stop the container (data is preserved)
docker compose down

# Stop and DELETE all data (fresh start)
docker compose down -v
```

## Resetting the Database

If you want to reload the CSV from scratch:

```bash
docker compose down -v
docker compose up -d
```

The `-v` flag removes the named volume, so Postgres reinitializes and reruns `init.sql`.
