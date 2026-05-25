import time
import csv

from pathlib import Path

from scripts.db.connect import connect
from scripts.load.timescale import load_timescale
from scripts.load.mobility import load_mobility


# Config

DATASETS = [
    "small",
    "medium",
    "large"
]

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = (
    BASE_DIR
    / "data/processed"
)

RESULTS_FILE = (
    BASE_DIR
    / "results/ingestion/ingestion_results.csv"
)


# Reset table
def reset_table(cur, table):

    cur.execute(
        f"TRUNCATE {table};"
    )


# Measure ingestion
def measure(func):

    start = time.perf_counter()

    count = func()

    end = time.perf_counter()

    duration = end - start

    throughput = (
        count / duration
        if duration > 0
        else 0
    )

    return duration, throughput, count


# Save benchmark result
def save(
    system,
    dataset,
    count,
    duration,
    throughput
):

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    file_exists = RESULTS_FILE.exists()

    with RESULTS_FILE.open(
        "a",
        newline=""
    ) as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow([
                "system",
                "dataset",
                "rows_or_sequences",
                "time_sec",
                "throughput_per_sec"
            ])

        writer.writerow([
            system,
            dataset,
            count,
            round(duration, 4),
            round(throughput, 2)
        ])


# Main
def main():

    # Reset previous results
    if RESULTS_FILE.exists():
        RESULTS_FILE.unlink()

    conn = connect()

    cur = conn.cursor()

    print("\n=== INGESTION BENCHMARK ===\n")

    for dataset in DATASETS:

        print(f"\nDataset: {dataset}")

        dataset_path = (
            DATA_DIR
            / f"{dataset}.csv"
        )

        ts_table = (
            f"readings_timescale_{dataset}"
        )

        mob_table = (
            f"readings_mobility_{dataset}"
        )

        # Timescale ingestion
        reset_table(
            cur,
            ts_table
        )

        conn.commit()

        print(
            f"Running Timescale ingestion → {ts_table}"
        )

        duration, throughput, count = measure(
            lambda: load_timescale(
                cur,
                dataset_path,
                ts_table
            )
        )

        conn.commit()

        print(
            f"Timescale: {duration:.2f} sec | "
            f"{throughput:.2f} rows/sec"
        )

        save(
            "timescale",
            dataset,
            count,
            duration,
            throughput
        )

        # Mobility ingestion
        reset_table(
            cur,
            mob_table
        )

        conn.commit()

        print(
            f"Running Mobility ingestion → {mob_table}"
        )

        duration, throughput, count = measure(
            lambda: load_mobility(
                cur,
                dataset_path,
                mob_table
            )
        )

        conn.commit()

        print(
            f"Mobility: {duration:.2f} sec | "
            f"{throughput:.2f} seq/sec"
        )

        save(
            "mobility",
            dataset,
            count,
            duration,
            throughput
        )

    cur.close()
    conn.close()

    print("\nIngestion benchmark complete.")
    print(f"Results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()