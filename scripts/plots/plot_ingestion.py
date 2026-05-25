import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "results/ingestion/ingestion_results.csv"
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


# Ingestion time
plt.figure()

for system in df["system"].unique():

    subset = df[
        df["system"] == system
    ]

    plt.plot(
        subset["dataset"],
        subset["time_sec"],
        marker="o",
        label=system
    )

plt.xlabel("Dataset size")
plt.ylabel("Time (seconds)")
plt.title("Ingestion Time")

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "ingestion_time.png"
)

plt.close()


# Throughput
plt.figure()

for system in df["system"].unique():

    subset = df[
        df["system"] == system
    ]

    plt.plot(
        subset["dataset"],
        subset["throughput_per_sec"],
        marker="o",
        label=system
    )

plt.xlabel("Dataset size")
plt.ylabel("Throughput")
plt.title("Ingestion Throughput")

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "ingestion_throughput.png"
)

plt.close()

print("Ingestion plots generated.")