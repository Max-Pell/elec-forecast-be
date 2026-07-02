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
    Retrieve the hourly temperature data for Brussels between `start` and `end` (inclusive), 
    and write the raw response to `data/raw/weather/`.
    Return the path to the written file.
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
    import argparse
    parser = argparse.ArgumentParser(
        description="Fetch raw hourly weather for Brussels into data/raw/weather/."
    )
    parser.add_argument("--start", default="2026-06-01", help="ISO date YYYY-MM-DD, inclusive")
    parser.add_argument("--end", default="2026-06-07", help="ISO date YYYY-MM-DD, inclusive")
    args = parser.parse_args()

    path = fetch_weather_raw(date.fromisoformat(args.start), date.fromisoformat(args.end))
    print(f"Weather raw saved in: {path}")