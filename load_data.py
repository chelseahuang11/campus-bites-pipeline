import csv
import psycopg2
from psycopg2.extras import execute_values

# --- Database connection settings ---
# Matches the credentials and database name defined in docker-compose.yml.
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "campus_bites",
    "user": "postgres",
    "password": "postgres",
}

# --- Path to the source CSV file ---
CSV_PATH = "data/campus_bites_orders.csv"

# --- Table definition ---
# Uses CREATE TABLE IF NOT EXISTS so the script is safe to run multiple times
# without erroring if the table already exists.
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS orders (
    order_id            INTEGER PRIMARY KEY,
    order_date          DATE,
    order_time          TIME,
    customer_segment    TEXT,
    order_value         NUMERIC(10, 2),
    cuisine_type        TEXT,
    delivery_time_mins  INTEGER,
    promo_code_used     TEXT,
    is_reorder          TEXT
);
"""

def load():
    # Read the CSV using Python's built-in csv module.
    # DictReader maps each row to a dict keyed by the header column names.
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                int(row["order_id"]),
                row["order_date"],
                row["order_time"],
                row["customer_segment"],
                float(row["order_value"]),
                row["cuisine_type"],
                int(row["delivery_time_mins"]),
                row["promo_code_used"],
                row["is_reorder"],
            )
            for row in reader
        ]

    # Open a connection to Postgres. The `with` block ensures the connection
    # is closed automatically when the block exits, even if an error occurs.
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            # Create the table if it doesn't already exist.
            cur.execute(CREATE_TABLE_SQL)

            # Clear any existing rows so re-running the script doesn't
            # produce duplicates. TRUNCATE is faster than DELETE for full reloads.
            cur.execute("TRUNCATE TABLE orders;")

            # Insert all rows in a single statement using execute_values.
            # This is significantly faster than inserting rows one at a time.
            execute_values(
                cur,
                """
                INSERT INTO orders (
                    order_id, order_date, order_time, customer_segment,
                    order_value, cuisine_type, delivery_time_mins,
                    promo_code_used, is_reorder
                ) VALUES %s
                """,
                rows,
            )

        # Commit the transaction. Without this, changes are rolled back
        # when the connection closes.
        conn.commit()
        print(f"Loaded {len(rows)} rows into orders.")

if __name__ == "__main__":
    load()
