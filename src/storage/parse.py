import json
from pathlib import Path
from datetime import datetime,timezone


def parse_weather_file(path:Path) -> list[tuple[datetime,str,float]]:
    """
    Read a weather file, parse it and return a list of tuple.
    """

    file = json.loads(path.read_text())

    series = file["hourly"]
    times = series["time"]
    values = series["temperature_2m"]

    parsed = []

    for i in range(len(times)):
        parsed.append((datetime.fromisoformat(times[i]).replace(tzinfo=timezone.utc),
                       "temperature_2m",
                       values[i]))


    return parsed


def parse_load_file(path:Path) -> list[tuple[datetime,str,float]]:
    """
    Read a load file, parse it and return a list of tuple.
    """
    file = json.loads(path.read_text())

    times = file["unix_seconds"]
    types = file["production_types"]
    loads = next((data for data in types if data["name"] == "Load"))["data"]

    parsed = [] 

    for i in range(len(times)):
        parsed.append((datetime.fromtimestamp(times[i],timezone.utc), 
                      "load",
                      loads[i]))

    return parsed


if __name__ == "__main__":
    path_weather = Path("/home/maxpell/projets/elec-forecast-be/data/raw/weather/weather_2025-06-01_2025-06-30.json")
    path_load = Path("/home/maxpell/projets/elec-forecast-be/data/raw/load/load_2024-01-01_2024-01-07.json")
    print(parse_load_file(path_load))

