import requests
from pathlib import Path
from datetime import date
from .http_client import get_with_retry


OPEN_METEO_API_URL = "https://archive-api.open-meteo.com/v1/archive"
BRUXELLES_LAT = 50.85
BRUXELLES_LONG = 4.35
TARGET_DIR = Path("./data/raw/weather")


def fetch_weather_raw(start:date, end:date) -> Path:
    """
    Recupere la temperature horaire a Bruxelles entre start et end (inclus)
    et ecrit la reponse brute dans data/raw/weather/.
    Retourne le chemin du fichier ecrit.
    """
    params = {
        "latitude":BRUXELLES_LAT,
        "longitude":BRUXELLES_LONG,
        "start_date":start.isoformat(),
        "end_date":end.isoformat(),
        "hourly":"temperature_2m"
    }

    TARGET_DIR.mkdir(parents=True,exist_ok=True)

    response = get_with_retry(OPEN_METEO_API_URL, params=params)
    
    file_path = TARGET_DIR / f"weather_{start}_{end}.json"

    with open(file_path, "w") as f:
        f.write(response.text)

    return file_path


if __name__ == "__main__":
    print("Raw data saved in : " f"{fetch_weather_raw(date(2025,6,1),date(2025,6,30))}")