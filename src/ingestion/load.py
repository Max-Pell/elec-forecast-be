# src/ingestion/load.py
from pathlib import Path
from datetime import date
from .http_client import get_with_retry

ENERGY_CHARTS_URL = "https://api.energy-charts.info/public_power"
TARGET_DIR = Path("data/raw/load")


def fetch_load_raw(start: date, end: date) -> Path:
    """
    Recupere production et charge de la zone BE entre start et end via
    Energy-Charts, et ecrit le brut (JSON) dans data/raw/load/.
    Retourne le chemin du fichier ecrit.
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
    chemin = fetch_load_raw(date(2024, 1, 1), date(2024, 1, 7))
    print("Ecrit dans:", chemin)