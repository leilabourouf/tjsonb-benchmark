import time
import csv
import statistics

from pathlib import Path

from scripts.db.connect import connect


BASE_DIR = Path(__file__).resolve().parents[2]

RESULTS_FILE = (
    BASE_DIR
    / "results/queries/query_results.csv"
)

QUERIES_DIR = (
    BASE_DIR
    / "sql/queries"
)

DATASETS = [
    "small",
    "medium",
    "large"
]

QUERY_FOLDERS = [
    "F1_temporal_window",
    "F2_threshold_filter",
    "F3_time_threshold",
    "F4_count_per_sensor",
    "F5_duration",
    "F6_global_time_range",
    "F7_latest_value",
    "F8_first_value",
    "F9_avg_humidity",
    "F10_window_avg_temp",
]

RUNS = 5


# Load SQL query
def load_query(path):

    return path.read_text().strip()


# Execute query once
def execute_query(cur, query):

    start = time.perf_counter()

    cur.execute(query)
    cur.fetchall()

    end = time.perf_counter()

    return end - start


# Warmup + benchmark
def benchmark_query(cur, query):

    # Warmup run
    cur.execute(query)
    cur.fetchall()

    times = []

    for _ in range(RUNS):

        duration = execute_query(
            cur,
            query
        )

        times.append(duration)

    median_time = statistics.median(times)

    return median_time


# Save benchmark result
def save_result(dataset, query_id, system, time_sec):

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    exists = RESULTS_FILE.exists()

    with RESULTS_FILE.open("a", newline="") as f:

        writer = csv.writer(f)

        if not exists:
            writer.writerow([
                "dataset",
                "query",
                "system",
                "time_sec"
            ])

        writer.writerow([
            dataset,
            query_id,
            system,
            round(time_sec, 6)
        ])


def main():

    # Reset previous results
    if RESULTS_FILE.exists():
        RESULTS_FILE.unlink()

    conn = connect()
    conn.autocommit = True

    cur = conn.cursor()

    print("\n=== QUERY BENCHMARK ===\n")

    print(f"Warmup runs: 1")
    print(f"Measured runs: {RUNS}")
    print(f"Statistic: median runtime")

    for dataset in DATASETS:

        print(f"\n--- {dataset.upper()} ---")

        for query_id in QUERY_FOLDERS:

            print(f"\n{query_id}")

            mobility_path = (
                QUERIES_DIR
                / query_id
                / "mobility.sql"
            )

            timescale_path = (
                QUERIES_DIR
                / query_id
                / "timescale.sql"
            )

            mobility_query = load_query(
                mobility_path
            ).format(size=dataset)

            timescale_query = load_query(
                timescale_path
            ).format(size=dataset)

            mobility_time = benchmark_query(
                cur,
                mobility_query
            )

            timescale_time = benchmark_query(
                cur,
                timescale_query
            )

            save_result(
                dataset,
                query_id,
                "mobility",
                mobility_time
            )

            save_result(
                dataset,
                query_id,
                "timescale",
                timescale_time
            )

            print(f"Mobility:  {mobility_time:.4f}s")
            print(f"Timescale: {timescale_time:.4f}s")

    cur.close()
    conn.close()

    print("\nQuery benchmark complete.")
    print(f"Results saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    main()