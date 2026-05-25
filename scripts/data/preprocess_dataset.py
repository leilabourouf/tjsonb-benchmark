import csv
import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data/raw/data.txt"
OUTPUT_FILE = BASE_DIR / "data/processed/small.csv"


def parse_line(line):
    parts = line.strip().split()

    if len(parts) < 8:
        return None

    try:
        timestamp = f"{parts[0]} {parts[1]}"
        sensor_id = parts[3]

        data = {
            "temperature": float(parts[4]),
            "humidity": float(parts[5]),
            "light": float(parts[6]),
            "voltage": float(parts[7]),
        }

        return sensor_id, timestamp, data

    except ValueError:
        return None


def preprocess():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    grouped = defaultdict(list)

    skipped = 0
    total = 0

    with INPUT_FILE.open("r") as f:
        for line in f:
            parsed = parse_line(line)

            if parsed is None:
                skipped += 1
                continue

            sensor_id, timestamp, data = parsed

            grouped[sensor_id].append((
                timestamp,
                data
            ))

            total += 1

    cleaned_rows = []

    for sensor_id, values in grouped.items():

        values.sort(
            key=lambda x: datetime.fromisoformat(x[0]).timestamp()
        )

        last_ts = None

        for ts, data in values:
            dt = datetime.fromisoformat(ts)

            if last_ts is not None and dt <= last_ts:
                continue

            cleaned_rows.append([
                sensor_id,
                ts,
                json.dumps(data)
            ])

            last_ts = dt

    with OUTPUT_FILE.open("w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "sensor_id",
            "timestamp",
            "data"
        ])

        writer.writerows(cleaned_rows)

    print("Preprocessing complete")
    print(f"Total raw rows: {total}")
    print(f"Skipped invalid rows: {skipped}")
    print(f"Final rows: {len(cleaned_rows)}")
    print(f"Sensors: {len(grouped)}")


if __name__ == "__main__":
    preprocess()