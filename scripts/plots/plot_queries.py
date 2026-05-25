import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "results/queries/query_results.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results/figures"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


df = pd.read_csv(INPUT_FILE)


query_names = {
    "F1_temporal_window": "Temporal Window",
    "F2_threshold_filter": "Threshold Filter",
    "F3_time_threshold": "Time + Threshold",
    "F4_count_per_sensor": "Count per Sensor",
    "F5_duration": "Duration",
    "F6_global_time_range": "Global Time Range",
    "F7_latest_value": "Latest Value",
    "F8_first_value": "First Value",
    "F9_avg_humidity": "Average Humidity",
    "F10_window_avg_temp": "Window Average Temperature"
}


for qid in df["query"].unique():

    subset = df[
        df["query"] == qid
    ]

    plt.figure()

    for system in subset["system"].unique():

        system_subset = subset[
            subset["system"] == system
        ]

        plt.plot(
            system_subset["dataset"],
            system_subset["time_sec"],
            marker="o",
            label=system
        )

    plt.title(
        query_names.get(qid, qid)
    )

    plt.xlabel("Dataset size")
    plt.ylabel("Execution time (seconds)")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"{qid}.png"
    )

    plt.close()

print("Query plots generated.")