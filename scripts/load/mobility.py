import csv
import json
from collections import defaultdict
from datetime import datetime


def load_mobility(cur, dataset_path, table):
    """
    Load CSV data into MobilityDB as tjsonb trajectories.

    Args:
        cur: database cursor
        dataset_path: path to CSV file
        table: target table name (e.g., readings_mobility_small)

    Returns:
        number of sequences inserted
    """

    grouped = defaultdict(list)

    # ----------------------------------------------
    # Step 1: Group rows by sensor_id
    # ----------------------------------------------
    with dataset_path.open("r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            grouped[row["sensor_id"]].append((
                row["timestamp"],
                row["data"]
            ))

    total_sequences = 0

    # ----------------------------------------------
    # Step 2: Build temporal sequences
    # ----------------------------------------------
    for sensor_id, values in grouped.items():

        # Sort timestamps
        values.sort(key=lambda x: datetime.fromisoformat(x[0]))

        # Remove duplicate timestamps
        seen = set()
        filtered = []

        for ts, json_data in values:
            if ts in seen:
                continue
            seen.add(ts)
            filtered.append((ts, json_data))

        # Build temporal instants
        instants_sql = []

        for ts, json_data in filtered:
            # Ensure valid JSON
            json_safe = json.dumps(json.loads(json_data))

            instants_sql.append(
                f"tjsonb('{json_safe}'::jsonb, '{ts}'::timestamptz)"
            )

        if not instants_sql:
            continue

        # ----------------------------------------------
        # Insert sequence into target table
        # ----------------------------------------------
        query = f"""
            INSERT INTO {table} (sensor_id, traj)
            VALUES (
                %s,
                tjsonbSeq(ARRAY[{",".join(instants_sql)}], 'discrete')
            )
        """

        cur.execute(query, (sensor_id,))
        total_sequences += 1

    return total_sequences