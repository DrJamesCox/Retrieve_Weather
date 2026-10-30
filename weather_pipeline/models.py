# models.py
# Original code from section "3. Database table" - moved as-is.
# DEFINITIONS layer: describes the shape of the database table. Imports
# nothing from the project.

import datetime
from sqlmodel import Field, SQLModel

# =================================================
# 3. Database table (SQLModel) - only what we want to store
# =================================================
# WHY A SEPARATE CLASS? In a SQLModel table (table=True), EVERY field becomes
# a column. Field(sa_column=None) does NOT exclude a field, because None is
# already the default. The clean way to store only some fields is to keep the
# API shape (CurrentWeather above) separate from the table shape (below).


class WeatherRecord(SQLModel, table=True):
    __tablename__ = "weather_history"

    # Add a database primary key id that isn't required in the API payload
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    # The 3 specific fields requested (Validated and stored)
    temperature: float  # celsius
    windspeed: float    # km/h
    winddirection: int  # degrees