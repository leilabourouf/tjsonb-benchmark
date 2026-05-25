import csv
from pathlib import Path
from datetime import datetime, timedelta


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data/processed/small.csv"

OUTPUT_MEDIUM = BASE_DIR / "data/processed/medium.csv"
OUTPUT_LARGE = BASE_DIR / "data/processed/large.csv"


def shift_timestamp(ts: str, offset_seconds: int) -> str:
    dt = datetime.fromisoformat(ts)
    return (dt + timedelta(seconds=offset_seconds)).isoformat(sep=" ")


def scale_dataset(input_path, output_path, multiplier):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open("r") as f_in, output_path.open("w", newline="") as f_out:

        reader = csv.DictReader(f_in)

        writer = csv.writer(f_out)

        writer.writerow([
            "sensor_id",
            "timestamp",
            "data"
        ])

        total_rows = 0

        for row in reader:

            original_sensor = row["sensor_id"]
            original_ts = row["timestamp"]
            data = row["data"]

            for i in range(multiplier):

                new_sensor_id = f"{original_sensor}_copy{i}"

                new_timestamp = shift_timestamp(
                    original_ts,
                    i
                )

                writer.writerow([
                    new_sensor_id,
                    new_timestamp,
                    data
                ])

                total_rows += 1

    print(f"Generated: {output_path}")
    print(f"Rows: {total_rows}")


def main():

    print("Generating medium dataset...")
    scale_dataset(
        INPUT_FILE,
        OUTPUT_MEDIUM,
        multiplier=5
    )

    print("\nGenerating large dataset...")
    scale_dataset(
        INPUT_FILE,
        OUTPUT_LARGE,
        multiplier=10
    )


if __name__ == "__main__":
    main()