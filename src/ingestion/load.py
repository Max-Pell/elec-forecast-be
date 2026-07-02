# src/ingestion/load.py
from pathlib import Path
from datetime import date
from .http_client import get_with_retry

ENERGY_CHARTS_URL = "https://api.energy-charts.info/public_power"
TARGET_DIR = Path("data/raw/load")


def fetch_load_raw(start: date, end: date) -> Path:
    """
    Retrieve the production and load data for the BE zone between `start` and `end` 
    from Energy-Charts, and write the raw JSON data to `data/raw/load/`.
    Return the path to the written file.
    """
    params = {
        "country":"be",
        "start":start.isoformat(),
        "end":end.isoformat()
    }

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    response = get_with_retry(ENERGY_CHARTS_URL,params=params)

    file_path = TARGET_DIR / f"load_{start}_{end}.json"

    with open(file_path, "w") as f:
        f.write(response.text)

    return file_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Fetch raw Belgian load into data/raw/load/."
    )
    parser.add_argument("--start", default="2026-06-01", help="ISO date YYYY-MM-DD, inclusive")
    parser.add_argument("--end", default="2026-06-07", help="ISO date YYYY-MM-DD, inclusive")
    args = parser.parse_args()

    path = fetch_load_raw(date.fromisoformat(args.start), date.fromisoformat(args.end))
    print(f"Load raw saved in: {path}")