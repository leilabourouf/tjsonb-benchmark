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
    "F1_temporal_window": "F1",
    "F2_threshold_filter": "F2",
    "F3_time_threshold": "F3",
    "F4_count_per_sensor": "F4",
    "F5_duration": "F5",
    "F6_global_time_range": "F6",
    "F7_latest_value": "F7",
    "F8_first_value": "F8",
    "F9_avg_humidity": "F9",
    "F10_window_avg_temp": "F10"
}


# Use only LARGE dataset for README overview
df = df[
    df["dataset"] == "large"
].copy()


df["query_label"] = df["query"].map(query_names)


pivot = df.pivot(
    index="query_label",
    columns="system",
    values="time_sec"
)


fig, ax = plt.subplots(
    figsize=(12, 5)
)


pivot.plot(
    kind="bar",
    ax=ax
)


ax.set_title(
    "Overall Query Performance (Large Dataset)"
)

ax.set_xlabel("Query")
ax.set_ylabel("Execution Time (seconds)")

# Important for readability because runtimes vary a lot
ax.set_yscale("log")

ax.legend(
    title="System"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "query_overview_large.png",
    dpi=300
)

plt.close()

print("Overview query plot generated.")