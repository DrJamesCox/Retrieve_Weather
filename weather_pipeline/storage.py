# storage.py
# Original code from sections "5.3" and "5.4" - moved as-is.
# WORKER layer: writes to and reads from the database.
# DATA IN: weather_report (a Weather object) from validate.py, handed over
#          by main.py
# DATA OUT: a new row in the SQLite file; print_db() reads rows back out.

from sqlmodel import Session, select

# ==========================================================
# >>> ADDED FOR DATA FLOW (START)
# ==========================================================
# The functions below use three names that used to sit in the same file.
# Each now lives in its own module, so each must be imported here:
#
#   engine        <- database.py : the connection to the SQLite file.
#                                  Both save and print use this ONE shared
#                                  engine, so they talk to the same database.
#   WeatherRecord <- models.py   : the table blueprint. Used to build a row
#                                  to save, and to tell select() which table
#                                  to read.
#   Weather       <- schemas.py  : the type of the object this module
#                                  RECEIVES from validate.py (via main.py).
#                                  Used in the type hint of
#                                  save_weather_report().
from weather_pipeline.database import engine
from weather_pipeline.models import WeatherRecord
from weather_pipeline.schemas import Weather # only for the type hint; not actually used
# ==========================================================
# <<< ADDED FOR DATA FLOW (END)
# ==========================================================


# 5.3 Save weather_report to DB
def save_weather_report(weather_report: Weather) -> None:
    """Copy the fields we care about into a table row and commit it."""
    current = weather_report.current_weather
    record = WeatherRecord(
        temperature=current.temperature,
        windspeed=current.windspeed,
        winddirection=current.winddirection,
    )

    with Session(engine) as session:
        session.add(record)
        session.commit()
        session.refresh(record)
        print(f"Record saved to DB: {record}")

# 5.4 Print the DB contents
def print_db():
    with Session(engine) as session:
        records = session.exec(select(WeatherRecord)).all()
        for record in records:
            print(record)