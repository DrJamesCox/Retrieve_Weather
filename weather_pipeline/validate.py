# validate.py
# Original code from section "5.2 Validate Weather" - moved as-is.
# WORKER layer: turns the raw dict into a validated Weather object.
# DATA IN:  response_dict (a dict) from fetch.py, handed over by main.py
# DATA OUT: weather_report (a Weather object) -> main.py passes it to storage.py

from pydantic import ValidationError

# ==========================================================
# >>> ADDED FOR DATA FLOW (START)
# ==========================================================
# validate_weather() calls Weather.model_validate(...). In the single-file
# version, Weather was defined a few lines above, so Python could find it.
# Now Weather lives in schemas.py, so this file must import it.
# This import is the "pipe" that brings the Weather blueprint from
# schemas.py into this file.
from weather_pipeline.schemas import Weather
# ==========================================================
# <<< ADDED FOR DATA FLOW (END)
# ==========================================================


# 5.2 Validate Weather: Validate JSON shape and data types
def validate_weather(response_dict: dict) -> Weather | None:
    try:
        weather_report = Weather.model_validate(response_dict)
        print("YAY!!!!")
        print(weather_report)
        print(type(weather_report)) # <class '__main__.Weather'
        return weather_report

    except ValidationError as e:
        print("Validation failed:", e.json())
        return None