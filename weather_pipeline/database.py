# database.py
# Original code from section "4. Database Configuration" - moved as-is.
# DEFINITIONS layer: owns the one shared "engine" (the connection to the
# SQLite file). Imports nothing from the project.

from sqlmodel import SQLModel, create_engine

# ==========================================================
# 4. Database Configuration
# ==========================================================
DATABASE_URL = "sqlite:///./weather_sqlmodel_2.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    """Builds the SQLite table layout out-of-the-box"""
    SQLModel.metadata.create_all(engine)