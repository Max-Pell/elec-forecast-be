from datetime import datetime
from src.storage.db import get_connection
from src.storage.parse import parse_weather_file, parse_load_file
from pathlib import Path

UPSERT_SQL = """
INSERT INTO observations (ts, series, value)
VALUES (%s, %s, %s)
ON CONFLICT (ts, series) DO UPDATE
SET value = EXCLUDED.value;
"""

def upsert_observations(rows : list[tuple[datetime,str,float]]):
    """
    Upsert the data in the database.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(UPSERT_SQL, rows)
            return len(rows)



if __name__ == "__main__":
    import argparse
    from datetime import date

    parser = argparse.ArgumentParser(
        description="Parse the raw load + weather files for a range and upsert into the DB."
    )
    parser.add_argument("--start", default="2026-06-01", help="ISO date YYYY-MM-DD, inclusive")
    parser.add_argument("--end", default="2026-06-07", help="ISO date YYYY-MM-DD, inclusive")
    args = parser.parse_args()

    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)

    load_path = Path("data/raw/load") / f"load_{start}_{end}.json"
    weather_path = Path("data/raw/weather") / f"weather_{start}_{end}.json"

    for p in (load_path, weather_path):
        if not p.exists():
            raise SystemExit(
                f"Missing raw file: {p}. Run the weather and load fetch commands "
                "for the same range first."
            )

    rows = parse_load_file(load_path)
    rows.extend(parse_weather_file(weather_path))
    count = upsert_observations(rows)
    print(f"Upserted {count} rows for {start} to {end}.")