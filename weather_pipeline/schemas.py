# Pydantic models: the shape of the API JSON
# schemas.py
# Original code from section "2. Validation Models" - moved as-is.
# DEFINITIONS layer: describes the shape of the API JSON. Imports nothing
# from the project, so any other module can safely depend on it.

from pydantic import BaseModel

# =================================================
# 2. Validation Models
# =================================================

class Current_Weather_Units(BaseModel):
    time: str
    interval: str
    temperature: str
    windspeed: str
    winddirection: str
    is_day: str
    weathercode: str

class Current_Weather(BaseModel):
    temperature: float
    windspeed: float
    winddirection: int
    time: str
    interval: int
    is_day: int
    weathercode: int

class Weather(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current_weather_units: Current_Weather_Units
    current_weather: Current_Weather