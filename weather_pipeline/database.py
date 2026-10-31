# database.py
# Original code from section "4. Database Configuration".
# DEFINITIONS layer: owns the one shared "engine" (the connection to the
# database). Imports nothing from the project.
#
# ==========================================================
# >>> CHANGED FOR MYSQL: this is the ONLY project file that changes.
# ==========================================================
# Every other module (storage.py, api.py, main.py) just imports "engine"
# from here. They never know which database is behind it, so swapping
# SQLite for MySQL happens in this one file. That is the payoff of
# keeping the database setup in its own module.

import os   # ADDED: reads the password from an environment variable
from sqlmodel import SQLModel, create_engine

# ==========================================================
# 4. Database Configuration
# ==========================================================

# --- OLD (SQLite): kept for comparison -------------------
# DATABASE_URL = "sqlite:///./weather_sqlmodel_2.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# --- NEW (MySQL) -----------------------------------------
# URL format:  dialect+driver://user:password@host:port/database_name
#   mysql+pymysql -> talk to MySQL using the PyMySQL driver
#   weather_db    -> the database must ALREADY exist (create it once in
#                    MySQL with:  CREATE DATABASE weather_db;)
#                    create_all() makes TABLES, not the database itself.
#
# The password is read from the MYSQL_PASSWORD environment variable so
# it never gets typed into the code (or committed to GitHub).
MYSQL_USER = "root"
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "weather_db"

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# connect_args={"check_same_thread": False} is REMOVED: it is a
# SQLite-only setting, and PyMySQL would reject it with an error.
# pool_pre_ping=True checks each connection before use, so the API
# server recovers if MySQL closes an idle connection overnight.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def init_db():
    """Builds the table layout out-of-the-box (unchanged)"""
    SQLModel.metadata.create_all(engine)
