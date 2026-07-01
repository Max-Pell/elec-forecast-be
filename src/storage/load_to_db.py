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
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(UPSERT_SQL, rows)
            return len(rows)

if __name__ == "__main__":
    path_weather = Path("/home/maxpell/projets/elec-forecast-be/data/raw/weather/weather_2025-06-01_2025-06-30.json")
    rows = parse_weather_file(path_weather)
    path_load = Path("/home/maxpell/projets/elec-forecast-be/data/raw/load/load_2024-01-01_2024-01-07.json")
    rows.extend(parse_load_file(path_load))
    upsert_observations(rows=rows)