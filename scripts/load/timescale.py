import csv
from psycopg2.extras import execute_batch


BATCH_SIZE = 5000


def load_timescale(cur, dataset_path, table):
    """
    Load CSV data into TimescaleDB using batched inserts.

    Args:
        cur: database cursor
        dataset_path: path to CSV file
        table: target table name (e.g., readings_timescale_small)

    Returns:
        number of rows inserted
    """

    total_rows = 0

    with dataset_path.open("r") as f:
        reader = csv.DictReader(f)

        batch = []

        for row in reader:
            batch.append((
                row["sensor_id"],
                row["timestamp"],
                row["data"]
            ))

            # Batch insert
            if len(batch) >= BATCH_SIZE:
                execute_batch(
                    cur,
                    f"""
                    INSERT INTO {table} (sensor_id, ts, data)
                    VALUES (%s, %s, %s::jsonb)
                    """,
                    batch
                )

                total_rows += len(batch)
                batch.clear()

        # Final batch
        if batch:
            execute_batch(
                cur,
                f"""
                INSERT INTO {table} (sensor_id, ts, data)
                VALUES (%s, %s, %s::jsonb)
                """,
                batch
            )

            total_rows += len(batch)

    return total_rows