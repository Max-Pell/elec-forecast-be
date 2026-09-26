# src/features/build_features.py
import pandas as pd
from datetime import datetime
from src.storage.db import get_connection

WIDE_QUERY = """
SELECT ts, series, value
FROM observations
WHERE ts >= %s AND ts < %s
ORDER BY ts;
"""


def load_wide(start: datetime, end: datetime) -> pd.DataFrame:
    """
    Lit les observations entre start et end et renvoie un DataFrame large,
    indexe par ts (UTC), avec une colonne par serie.
    """
    results = []

    with get_connection() as conn:
        with conn.cursor() as cursor:
            results = cursor.execute(WIDE_QUERY, (start, end)).fetchall()

    if not results:
        raise ValueError("Failed to read the database")

    df = pd.DataFrame(results, columns = ["ts", "series", "value"])
    df = df.set_index("ts")
    df = df.pivot(columns="series", values="value")

    return df


if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description="Parse the raw load + weather files for a range and upsert into the DB."
    )
    parser.add_argument("--start", default="2023-01-01", help="ISO date YYYY-MM-DD, inclusive")
    parser.add_argument("--end", default="2024-12-31", help="ISO date YYYY-MM-DD, inclusive")
    args = parser.parse_args()

    start = datetime.fromisoformat(args.start)
    end = datetime.fromisoformat(args.end)

    df = load_wide(start=start, end=end)
    print(df.head(30))

