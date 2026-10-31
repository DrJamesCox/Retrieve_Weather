# api.py
# ==========================================================
# >>> NEW FILE: the web API server (WORKER layer)
# ==========================================================
# This module lets OTHER programs (a browser, Postman, another script)
# read and add weather records over HTTP, instead of running main.py.
#
# It sits in the same layer as fetch.py / validate.py / storage.py:
# it imports the blueprints (models, database), and nothing imports it.
#
# Run it from the project root (the folder that holds main.py):
#     uvicorn weather_pipeline.api:app --reload
# Then open:  http://127.0.0.1:8000/docs   (interactive test page)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

# ----------------------------------------------------------
# DATA FLOW: reuse the SAME engine and table as the pipeline.
# Because api.py and storage.py share database.py's engine, records
# saved by main.py show up here, and records POSTed here show up in
# print_db(). One database, two ways in.
# ----------------------------------------------------------
from weather_pipeline.database import engine, init_db
from weather_pipeline.models import WeatherRecord


# ----------------------------------------------------------
# Request body for POST: what a client is ALLOWED to send.
# The client sends only the 3 readings. id and created_at are left
# out on purpose, so the database and the default_factory fill them
# in, exactly as they do when main.py saves a record.
# ----------------------------------------------------------
class WeatherRecordCreate(BaseModel):
    temperature: float   # celsius
    windspeed: float     # km/h
    winddirection: int   # degrees


# ----------------------------------------------------------
# The app object. "uvicorn weather_pipeline.api:app" means:
# "in the module weather_pipeline/api.py, run the object named app".
# ----------------------------------------------------------
app = FastAPI(title="Weather Records API")

# Make sure the weather_history table exists before any request arrives.
# This runs once, when uvicorn loads this file. It works because
# models.py was imported above (see the init_db note in main.py).
init_db()


# GET /weather -> list every stored record
@app.get("/weather", response_model=list[WeatherRecord])
def list_weather():
    with Session(engine) as session:
        return session.exec(select(WeatherRecord)).all()


# GET /weather/{record_id} -> one record, or 404 if it doesn't exist
@app.get("/weather/{record_id}", response_model=WeatherRecord)
def get_weather(record_id: int):
    with Session(engine) as session:
        record = session.get(WeatherRecord, record_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return record


# POST /weather -> add a record from the JSON body, return the saved row
@app.post("/weather", response_model=WeatherRecord, status_code=201)
def create_weather(data: WeatherRecordCreate):
    # Same steps as save_weather_report() in storage.py:
    # build a WeatherRecord, add, commit, refresh to get the new id.
    record = WeatherRecord(
        temperature=data.temperature,
        windspeed=data.windspeed,
        winddirection=data.winddirection,
    )
    with Session(engine) as session:
        session.add(record)
        session.commit()
        session.refresh(record)
        return record