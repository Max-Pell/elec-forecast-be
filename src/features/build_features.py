# src/features/build_features.py
import pandas as pd
from datetime import datetime, timezone
from src.storage.db import get_connection
import holidays

WIDE_QUERY = """
SELECT ts, series, value
FROM observations
WHERE ts >= %s AND ts < %s
ORDER BY ts;
"""

"""
Constant to set a minimal horizon limit under wich we can"t use data to predict the actual value.
We predict the load for the hour t when the hour t - HORIZON is completed.
"""
HORIZON = 24


def load_wide(start: datetime, end: datetime) -> pd.DataFrame:
    """
    Read the observations between start and end and return a
    wide DataFrame indexed by ts (UTC), with a column per serie.
    """
    results = []

    with get_connection() as conn:
        with conn.cursor() as cursor:
            results = cursor.execute(WIDE_QUERY, (start, end)).fetchall()

    if not results:
        raise ValueError("Failed to read the database")

    df = pd.DataFrame(results, columns=["ts", "series", "value"])
    df = df.set_index("ts")
    df = df.pivot(columns="series", values="value")

    return df


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des colonnes calendaires derivees de l'index temporel.
    """
    df = df.copy()
    assert isinstance(df.index, pd.DatetimeIndex)
    local = df.index.tz_convert("Europe/Brussels")
    df["hour"] = local.hour
    df["dayofweek"] = local.dayofweek
    df["month"] = local.month
    df["is_weekend"] = local.dayofweek >= 5
    be_holidays = holidays.Belgium()
    df["is_holiday"] = [d.date() in be_holidays for d in local]
    return df


def add_lag_features(
    df: pd.DataFrame, col: str = "load", lags=(24, 168), min_shift: int = HORIZON
) -> pd.DataFrame:
    """
    Add lags columns `col`. 24 = one day, 168 = one week.
    """
    assert isinstance(df.index, pd.DatetimeIndex)
    df = df.copy()

    for lag in lags:
        if lag < min_shift:
            raise ValueError(
                f"Temporal leak risk, the lag of {lag} is smaller than the minimal shift of {min_shift}"
            )

        df[f"{col}_lag_{lag}"] = df[col].shift(lag)

    return df


def add_rolling_features(
    df: pd.DataFrame, col: str = "load", windows=(24, 168), min_shift: int = HORIZON
) -> pd.DataFrame:
    """
    Ajoute des moyennes glissantes de `col` sur les fenetres donnees.
    `min_shift` = horizon de prevision : la fenetre se termine a t - min_shift.
    """
    df = df.copy()
    for w in windows:
        df[f"{col}_rollmean_{w}"] = df[col].shift(min_shift).rolling(w).mean()
    return df


#############--------------------------------------------------------------------

FEATURES_BUILD_LIST = (add_calendar_features, add_lag_features, add_rolling_features)


def build_features(
    df: pd.DataFrame, features_functions: tuple = FEATURES_BUILD_LIST
) -> pd.DataFrame:
    """
    Apply all the features building funcitons and build the dataframe.
    Drop the NAN rows except for the load column because it is the target.
    """
    for function in features_functions:
        df = function(df)
    colmuns_to_dropna = [col for col in df.columns if col != "load"]
    return df.dropna(subset=colmuns_to_dropna)


if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(
        description="Load the laod and weather data from the DB and build the large table with the calendars features."
    )
    parser.add_argument(
        "--start", default="2023-01-01", help="ISO date YYYY-MM-DD, inclusive"
    )
    parser.add_argument(
        "--end", default="2025-01-01", help="ISO date YYYY-MM-DD, exclusive"
    )
    args = parser.parse_args()

    start = datetime.fromisoformat(args.start).replace(tzinfo=timezone.utc)
    end = datetime.fromisoformat(args.end).replace(tzinfo=timezone.utc)

    df = build_features(load_wide(start=start, end=end))

    print(df.head())
