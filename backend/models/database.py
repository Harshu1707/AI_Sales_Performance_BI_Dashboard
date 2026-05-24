import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "insightiq.db"


def get_connection():
    return sqlite3.connect(DB_PATH)
