from pathlib import Path
import shutil
import kagglehub


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data/raw"


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading dataset...")

    dataset_path = kagglehub.dataset_download(
        "divyansh22/intel-berkeley-research-lab-sensor-data"
    )

    dataset_path = Path(dataset_path)

    for file in dataset_path.iterdir():
        if file.is_file():
            shutil.copy(file, RAW_DIR / file.name)

    print(f"Dataset copied to: {RAW_DIR}")


if __name__ == "__main__":
    main()