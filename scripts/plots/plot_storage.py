import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    BASE_DIR
    / "results/storage/storage_results.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results/figures"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Load results
df = pd.read_csv(INPUT_FILE)

# Dataset order
order = ["small", "medium", "large"]

components = [
    "table_mb",
    "index_mb",
    "toast_mb"
]


# Plot storage breakdown
for system in ["mobility", "timescale"]:

    plt.figure()

    subset = df[df["system"] == system]

    for component in components:

        y = [
            subset[
                subset["dataset"] == d
            ][component].values[0]
            for d in order
        ]

        plt.plot(
            order,
            y,
            marker="o",
            label=component.replace("_mb", "")
        )

    plt.title(f"{system} storage breakdown")

    plt.xlabel("Dataset size")
    plt.ylabel("MB")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"{system}_storage.png"
    )

    plt.close()

print("Storage plots generated.")